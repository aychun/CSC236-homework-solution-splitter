# from __future__ import annotations
import PyPDF2
from PyPDF2 import PageObject
import re
import os
from pathlib import Path
import datetime
from typing import List, Dict, Optional, Tuple


class HWsplitter:

    pages: List[PageObject]
    contents: List[str]
    filename: str
    filePath: str

    def __init__(self, filename: str, filePath: Optional[str] = None) -> None:
        self.filename = filename
        self.filePath = filePath
        reader = PyPDF2.PdfFileReader(filePath)
        self.pages = [reader.getPage(n) for n in range(reader.getNumPages())]
        self.contents = []

        self._updateContents()

    def _updateContents(self):
        for p in self.pages:
            self.contents.append(p.extractText())

        return None

    def extractQuestions(self) -> List[str]:
        questions = set()
        for c in self.contents:
            q = re.findall("Question \d\S", c)
            if q != []:
                questions.update(q)

        qs = list(questions)
        qs = [s[s.index(" ") + 1 :] for s in qs]

        out = []

        for c in self.contents:
            q = HWsplitter._getQuestionFromContent(c)
            if q in qs:
                out.append(q)

        out.sort()

        return out

    def extractQuestionPageNums(self) -> List[int]:

        pages = []
        qs = self.extractQuestions()
        for i, c in enumerate(self.contents):
            q = HWsplitter._getQuestionFromContent(c)
            if q in qs:
                pages.append(i)

        return pages

    def extractSolutionPageNums(self) -> Dict[str, Tuple[int]]:
        out = {}
        qs = self.extractQuestions()
        qsPageNums = self.extractQuestionPageNums()

        for i, c in enumerate(self.contents):
            q = HWsplitter._getQuestionFromContent(c)
            if q in qs[:-1]:  # disregard the last question for simpicity
                l = self._findSolutionLength(i, qs, qsPageNums)
                pages = tuple(j for j in range(i, i + l))
                out[q] = pages

            elif q in qs[-1:]:  # last question case
                out[q] = tuple(k for k in range(i, len(self.contents)))

        return out

    def _findSolutionLength(
        self, startingPageNum: int, qs: List[str], questionPagesNums: List[int]
    ) -> int:

        nextContent = self.contents[startingPageNum + 1]

        l = 1
        while HWsplitter._getQuestionFromContent(nextContent) not in qs:
            if startingPageNum + l in questionPagesNums:
                break
            nextContent = self.contents[startingPageNum + 1 + l]
            l += 1

        return l

    @staticmethod
    def _getQuestionFromContent(content: str) -> str:
        return content[:2]

    def __getSolutionPagesDict(self) -> Dict[str, List[PageObject]]:
        out = {}
        pageNums = self.extractSolutionPageNums()
        for k, v in pageNums.items():  # str, Tuple[int]
            pages = [self.pages[i] for i in v]
            out[k] = pages

        return out

    def __writePDFfileFromPages(self, pages: List[PageObject], filePath) -> None:
        """
        PyPDF2 writer seems to have a bug where the .write() method
        doesn't work properly when it's called inside a loop
        (https://stackoverflow.com/questions/40168027/pypdf2-pdffilewriter-has-no-attribute-stream)
        """

        writer = PyPDF2.PdfFileWriter()

        for p in pages:
            writer.addPage(p)

        with open(filePath, "wb") as out:
            writer.write(out)

        out.close()

        return None

    def Split(self) -> None:

        dt = datetime.datetime.now()
        currentTime = dt.strftime("%Y-%m-%d %H.%M.%S")

        dir = self.filename[:-4] + "_" + currentTime

        cwd = os.getcwd()
        path = Path(cwd + "/" + dir)
        os.mkdir(path)

        pageNums = self.extractSolutionPageNums()

        count = 0

        for q, nums in pageNums.items():
            filePath = Path(cwd + "/" + dir + "/" + q + ".pdf")

            reader = PyPDF2.PdfFileReader(self.filePath)
            writer = PyPDF2.PdfFileWriter()

            for n in nums:

                writer.addPage(reader.getPage(n))

            with open(filePath, "wb") as out:
                writer.write(out)
                count += 1

        print(f"Folder created at {path} containing your solutions")

        if count != len(self.extractQuestions()):
            print("\n WARNING \n some solutions have not been created\n")
            excluded = set(self.extractQuestions()).difference(
                set([k for k in pageNums.keys()])
            )
            excluded = list(excluded)
            excluded.sort()
            print(f"Please check the following questions: {excluded}")
            print("Make sure each solution starts with its own page")

    @staticmethod
    def pathToFilename(path: str) -> str:
        p = Path(path)
        if "\\" in str(p) or "/" in str(p):
            index = max(path.rfind("\\"), path.rfind("/"))
            return path[index + 1 :]
        else:
            return path
