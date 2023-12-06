function testOnDrive() {
  const items = {
    drive:{
      selectedItems:[
        {id: 'foo',
        title:'bar'}
      ]
    }
  }
  result = onDriveItemsSelected(items)
  console.log(JSON.stringify(result))
}


function onDriveItemsSelected(e) {
  var builder =  CardService.newCardBuilder();

  // For each item the user has selected in Drive, display either its
  // quota information or a button that allows the user to provide
  // permission to access that file to retrieve its quota details.
  e['drive']['selectedItems'].forEach(
    function(item){
      var cardSection = CardService.newCardSection()
          .setHeader(item['title'])
          .addWidget(CardService.newTextParagraph().setText(
                  'Open a Python Script in WebVPython'))

      var button = CardService.newTextButton()
        .setText("Open " + item['title'] + " in WebVPython")
        .setOpenLink(CardService.newOpenLink()
            .setUrl("https://glowscript.org/#api/gdID/" + item['id'])
            .setOpenAs(CardService.OpenAs.FULL_SIZE)
            .setOnClose(CardService.OnClose.NOTHING));

      cardSection.addWidget(button);
            
      builder.addSection(cardSection);
      console.log('done')

    });

  return builder.build();
}


