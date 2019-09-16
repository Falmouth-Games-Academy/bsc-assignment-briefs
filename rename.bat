For /R %%D IN (.) do (
cd %%D
ren *.tex build.tex
)
