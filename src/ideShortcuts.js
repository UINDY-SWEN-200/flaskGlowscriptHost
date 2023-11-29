import './ide';

function pagesShortcut() {
    function checkDialog(cb) {
        if ($dialog) {
            if (navigatingTo.program !== program || navigatingTo.page == "run") {
                $dialog.dialog("close")
            } else {
                // Keep the dialog on this page, but check again at the next transition
                onNavigate.on( checkDialog )
            }
        }
        cb()
    }

    function screenshot(ev) {
        sendMessage(JSON.stringify({ screenshot: true }))
        ev.preventDefault()
    }

    function sendEvent(ev) {
        // Forward some key events to the iframe, since otherwise it might not get them depending on focus
        // TODO: This is far from perfect.  The iframe receives many events twice, the right context menu is not blocked
        // when a right-spin drag begins inside the iframe but ends outside, not all event data is forwarded, etc.
        if (ev.type == "keydown" || ev.type == "keyup") ev = { type:ev.type, which:ev.which }
        else return;
        if (ready)
            sendMessage( JSON.stringify({event: ev}) )
    }
    // Wrapper for postMessage that queues messages while the iframe initializes
    function sendMessage(message) {
        if (unsentMessages === null)
            untrusted_frame.get(0).contentWindow.postMessage(message, untrusted_origin)
        else
            unsentMessages.push(message)
    }
    function findLine(line,w) {
        // w.indent is the indentation of javascript code by the GlowScript wrapping.
        var indent = w.indent+' ' // Error messages indent an additional space
        indent = new RegExp('^'+indent)
        line = line.replace(indent, '')
        var match = '', best = null, test
        for (var n=0; n<sourceLines.length; n++) {
            // Compiler changes "var a = 10" -> "a = 10" (with "var a" placed at top of program):
            test = sourceLines[n].replace(/^var\s*/, '') 
            for (var i=0; i<line.length; i++) {
                if (i >= test.length) break
                var c = line.charAt(i), t = test.charAt(i)
                if (c != t) break
            }
            if (i > match.length) {
                match = test.substring(0,i)
                best = n
            }
        }
        return best+1
    }
    function insertLineNumbers(errline) { // simplifed version of the same routine in compiler.js
        var lines = sourceLines
        var comment = false
        var lineno = 0
        for (var n=2; n<lines.length-1; n++) {
            var m = lines[n].match(/^\s*(.*)/)
            var line = m[1]
            if (line.substr(0,3) == '###') {
                comment = !comment
                continue
            }
            if (comment) continue
            if (line.length == 0 || line.charAt(0) == '#') continue
            lineno += 3
            if (lineno >= (errline-2)) return n
        }
        return -1
    }
    function receiveMessage(event) {
        event = event.originalEvent // originalEvent is a jquery entity
        // CAREFUL: We can't trust this data - it could be malicious! Incautiously splicing it into HTML could be deadly.
        if (event.origin !== untrusted_origin) return // check the origin
        var message = JSON.parse(event.data)
            
        // Angus Croll: javascriptweblog.wordpress.com/2011/08/08/fixing-the-javascript-typeof-operator/
        // {...} "object"; [...] "array"; new Date "date"; /.../ "regexp"; Math "math"; JSON "json";
        // Number "number"; String "string"; Boolean "boolean"; new ReferenceError) "error"
        var toType = function(obj) {
            return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
        }

        if (!ready) { // first-time message from run.js; check that first-time message content is {ready:true}
            if (toType(message) != 'object') return
            if (message.ready === undefined) return
            if (message.ready !== true) return
            delete message.ready
            for (var m in message) return // message should now be empty; if not, return
            ready = true
            if (unsentMessages !== null) {
                var um = unsentMessages; unsentMessages = null
                for (var i = 0; i < um.length; i++)
                    sendMessage(um[i])
            }
            if (isWritable) page.find(".prog-screenshot.button").removeClass("template").click( screenshot )
        }
        if (message.screenshot && isWritable && (!message.autoscreenshot || !haveScreenshot)) {
            haveScreenshot = true
            apiPut( {user:username, folder:folder, program:program}, { screenshot: message.screenshot }, function(){} )
        }
        if (message.error) {
            // Only Chrome (Aug. 2012) gives line numbers in error messages!
            var syntaxpattern = /(SyntaxError[^\d]*)([\d]*)/
            var findsyntax = message.error.match(syntaxpattern)
            if (findsyntax === null && parseVersionHeader(null).lang == 'javascript') {
                var u = message.error.split('\n')
                var m = u[0].match(/:(\d*):\d*:.*:(.*)/)
                if (m !== null) {
                    message.error = 'Error in line '+(m[1]-5)+':'+m[2]
                    message.traceback = u[1]+'\n'+u[2]
                }                    
            }
            if ($dialog) $dialog.dialog("close")
            $dialog = $("#program-error-dialog").clone().removeClass("template")
            $dialog.find(".error-details").text(message.error)
            $dialog.find(".error-traceback").text(message.traceback)
            $dialog.dialog({ width: "600px", autoOpen: true })
        }
    }
}