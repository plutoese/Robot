# coding=UTF-8

# --------------------------------------------------------------
# class_article文件
# @class: Article
# @introduction: Article类用来创建latex文档
# @dependency: pylatex模块
# @author: plutoese
# @date: 2016.02.18
# --------------------------------------------------------------


import re
from libs.latex.class_latexdoc import LatexDoc
from libs.latex.class_latexfromtemplate import LatexFromTemplate


class Article:
    """ Article类用来创建latex文档

    """
    def __init__(self,tex_template,replace_word=None):
        self.__doc = LatexDoc(document=LatexFromTemplate(tex_template,replace_word).document)

    @property
    def document(self):
        return self.__doc


if __name__ == '__main__':
    replace_word = {'articleTitle':'计量经济学',
                    'arcticleabstract':'发展农业、造福农村、富裕农民是习近平始终萦绕心头的“三农梦”。在2015年中央农村工作会议上，习近平再次强调，任何时候都不能忽视和放松“三农”工作，“十三五”时期，必须坚持把解决好“三农”问题作为全党工作重中之重。'}
    doc = Article(r'E:\latex\template\article_template_02.tex',replace_word)
    doc.document.append("当今世界正处于大变化、大调整的变革时期，中国的社会主义革命、建设和改革也进入了新的历史发展阶段。复兴马克思哲学，真正理解马克思对旧哲学的批判实质，将使我们的伟大实践更上层楼，更将使我们的哲学站在时代的最前沿，真正掌握马克思主义的话语权，推动全社会的进步发展。")
    doc.document.add_section("我的第三级章节",3)
    doc.document.add_section("我的第二级章节",2)
    doc.document.add_section("我的第三级章节2",3)
    doc.document.add_list(['我的列表','你的列表'],type=2)
    doc.document.add_table([['变量', '第一产业占GDP的比重_(全市)', '第一产业占GDP的比重_$市辖区','我错了'],[1,2,3,4],[5,6,7,8]])
    doc.document.add_figure(file='d:/down/europe.jpg',caption="Europe")
    doc.document.add_pretty_table(data=[['name','gender','age'],['Tom','Male',24],['Marry','Female',19]])
    doc.document.generate_tex(r'E:\latex\winwin')
    doc.document.generate_pdf(r'E:\latex\winwin')



