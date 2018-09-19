'''
impdf2txtdoc.py

Copyright (c) 2018, Stephen Pollett
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

'''
Tool for converting an image pdf to a textfile
'''
import io
import sys

from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
from ezodf import newdoc, Paragraph, Heading, Sheet

class pdffile():

    image = []
    text = []

    def __init__(self,f):
        self.tools = pyocr.get_available_tools()[0]
        self.lang = self.tools.get_available_languages()[0]
        self.pdff = Image(filename=f,resolution=300)
        self.pdfjpeg = self.pdff.convert('jpeg')

    def get_pages(self):
        for img in self.pdfjpeg.sequence:
            pages = Image(image=img)
            self.image.append(pages.make_blob('jpeg'))
    
    def get_text(self):
        for img in self.image:
            txt = self.tools.image_to_string(PI.open(io.BytesIO(img)),lang=self.lang,builder=pyocr.builders.TextBuilder())
            self.text.append(txt)



def main():
    fname = sys.argv[1]
    pf = pdffile(fname)
    pf.get_pages()
    pf.get_text()
    #print pf.text
    odt = newdoc(doctype='odt',filename=fname+'.odt')
    odt.body += Paragraph(pf.text)
    odt.save()

if(__name__ == '__main__'):
    main()