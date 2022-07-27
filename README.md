# CSC236-homework-solution-splitter
Python code to split a .pdf file to make it easier to be submitted on Crowdmark. 

## Instruction
- Make sure the latest version of [PyPDF2](https://pypi.org/project/PyPDF2/) (2.4.1>=) is installed
- Download your completed homework file from Overleaf or other Latex editor (download the entire document including the questions)
- Make sure `main.py`, `HWsplitter.py`, and `gui.py` are all in the same directory
- Run `main.py` 
- Select your file
- A folder containing your splitted solutions will be created

<p align="center">
  <img src=https://user-images.githubusercontent.com/85460898/176977299-7db4eb10-28f9-4d1c-9959-dc60baf1229b.png />
</p>


##  Known Bugs
- Any extra credit questions will be combined with the last non-extra question

## Updates
- Changed extractQuestions() and extractQuestionPageNums() in `HWsplitter.py` to correctly extract questions from the file (July/27/2022)