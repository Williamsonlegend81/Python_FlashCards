There are few Bugs present in the Project.
1. In the case you want to set font into italic or bold and revert the text back in normal mode then you need to select the text from left to right **(move cursor from left to right)** then only you will be apply
   to perform the operation. That's how **textCursor.hasSelection()** commands operates here.
2. In case you need to insert an attachment to the front or back section of the card. It will be inserted to both the parts of the card. So you want to keep image in either of part of the card then you need to
   delete it.
3. Stats button is unoperationle for now.
