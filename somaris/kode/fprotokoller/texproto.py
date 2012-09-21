#!/usr/bin/python

template = file("template.tex","r").read()

protokol = file("fields_WB_FDG_PET_CT_5.MlAdult","r").read()

output = template + "\\section{Topogram}\n\\subsection{Routine}\nJeg ved en laerkerede\n" + "\\end{document}"
print output
