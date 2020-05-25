% A document class for assignment briefs for BSc Computing for Games at Falmouth University

% Based on the article class
\LoadClass[a4paper]{article}

% Load required packages
\usepackage{tikz}      % For fancy graphics and positioning
\usepackage{xcolor}    % For colours
\usepackage{environ}   % Required for NewEnviron definitions in this file
\usepackage{pdflscape} % For landscape pages
\usepackage{longtable} % For >1 page marking rubric
\usepackage{colortbl}  % For colouring table cells
\usepackage{microtype} % For improved hyphenation
\usepackage{calc}
\usepackage{etoolbox}

\usepackage[hyphens]{url}


%\usepackage[pdftex, pdflang={en-GB}, pdfdisplaydoctitle]{hyperref} % For hyperlinks and also for PDF information

%\usepackage{pdfcomment}

% Adjust margins
\usepackage[margin=1.5cm, left=6.5cm]{geometry}
\setlength{\marginparwidth}{4.5cm}
\setlength{\marginparsep}{0.5cm}

% Disable page numbers
\pagestyle{empty}

% Set the font
\usepackage{avant}
\renewcommand{\familydefault}{\sfdefault}

% Put margin notes on the left hand side
\reversemarginpar

% Add spacing between paragraphs, and no indentation
\setlength{\parindent}{0em}
\setlength{\parskip}{1em}

% Adjust section title spacing
\usepackage{titlesec}
\titlespacing{\section}{0cm}{\parskip}{0cm}
\titlespacing{\subsection}{0cm}{\parskip}{0cm}

\usepackage[pdftex, pdflang={en-GB}, pdfdisplaydoctitle]{hyperref}

% Accessibility package is very particular about usepackage order so it goes here
%\usepackage[tagged, flatstructure]{accessibility}
\usepackage{tagpdf}
\tagpdfsetup{activate-all=true, 
interwordspace=true, 
newattribute = {UpperAlpha}{<</O /List /ListNumbering /UpperAlpha>>}, 
newattribute = {LowerRoman}{<</O /List /ListNumbering /LowerRoman>>},
newattribute = {Decimal}{<</O /List /ListNumbering /Decimal>>}}

% Make enumerate / itemize lists more closely spaced
\usepackage{enumitem}
\setlist{nosep}

% Fix for pound sterling sign http://tex.stackexchange.com/a/17858
\usepackage[T1]{fontenc} 

% For UNICODE characters
\usepackage[utf8]{inputenc}

% For adding todos and coloured boxes
\usepackage{todonotes}

% Allow document version to be specified, e.g. \version{1.1} in the preamble
% Defaults to 1.0 if not specified
\newcommand{\@version}{1.0}
\newcommand{\version}[1]{\renewcommand{\@version}{#1}}

% Allow module code to be specified, e.g. \module{COMP110} in the preamble
% Defaults to COMPXXX if not specified
\newcommand{\@module}{COMPXXX}
\newcommand{\module}[1]{\renewcommand{\@module}{#1}}

% Structure tagging for accessibility
% This macro sets the actualtext key --- may be needed in some situations where screen readers can't automatically extract text
\newcommand{\tagWithActualText}[2]{
    % Temporarily replace formatting macros with no-ops
    \begingroup
        \def\textbf{}
        \def\textit{}
        \def\emph{}
        \def\par{}
        \def\thinspace{ }
        % Expand and store the plain text
        \protected@xdef\tmpActualText{#2}
    % Restore formatting macros
    \endgroup
    % Create the structure tags
    \tagstructbegin{tag=#1, actualtext-o=\tmpActualText}
        \tagmcbegin{tag=#1}
            % Display the actual content
            #2
        \tagmcend
    \tagstructend
}

% Structure tagging for accessibility
\newcommand{\tag}[2]{
    % Create the structure tags
    \tagstructbegin{tag=#1}
        \tagmcbegin{tag=#1}
            % Display the actual content
            #2
        \tagmcend
    \tagstructend
}

% Shortcut to tag a paragraph
\newcommand{\p}[1]{\tag{P}{#1}}

% Overriding list environments with accessibility tagging
\newtoggle{LIOpen}
\global\togglefalse{LIOpen}

\newcounter{NestedEnumDepth}
\setcounter{NestedEnumDepth}{0}

\newcommand{\closeItem}
{
        \closeLBodyContainer %LBody
        \tagstructend %LBody
        \tagstructend %LI
        \global\togglefalse{LIOpen}
}

  %
  \let\originalenumerate\enumerate%
  \let\originalendenumerate\endenumerate%
  \renewenvironment{enumerate}%
    {
      \setcounter{NestedEnumDepth}{\value{NestedEnumDepth}+1}
      \ifnumcomp{\value{NestedEnumDepth}}{=}{1}{\tagstructbegin{tag=L, attribute={UpperAlpha}}}{}
      \ifnumcomp{\value{NestedEnumDepth}}{>}{1}{ \tagstructbegin{tag=L, attribute={LowerRoman}} \tagstructbegin{tag=LI} \tagstructbegin{tag=LBody}}{}
      \originalenumerate
    }{
     \originalendenumerate 
     \iftoggle{LIOpen}{\closeItem}{}
     \ifnumcomp{\value{NestedEnumDepth}}{=}{1}{\tagstructend}{}
      \ifnumcomp{\value{NestedEnumDepth}}{>}{1}{\tagstructend \tagstructend \tagstructend}{}
     \setcounter{NestedEnumDepth}{\value{NestedEnumDepth}-1}
     }%

    %
  \let\originalitemize\itemize%
  \let\originalenditemize\enditemize%
  \renewenvironment{itemize}%
    {
    \iftoggle{LIOpen}{\closeItem}{}
    \tagstructbegin{tag=L}
    \originalitemize
    }{
    \originalenditemize 
    \iftoggle{LIOpen}{\closeItem}{}
    \tagstructend}%
  %

\let\originaltheenumi\theenumi%
\renewcommand{\theenumi}{
    \originaltheenumi    
}

\newtoggle{LBodyContainerOpen}
\global\togglefalse{LBodyContainerOpen}

\newtoggle{RequireLBodyRestore}
\global\togglefalse{RequireLBodyRestore}

\newcommand{\openLBodyContainer}{
  \tagmcbegin{tag=LBody}
   \global\toggletrue{LBodyContainerOpen}
}

\newcommand{\closeLBodyContainer}{
  \tagmcend %LBody
   \global\togglefalse{LBodyContainerOpen}
}

\renewcommand{\labelitemi}{
    \iftoggle{LIOpen}{\closeItem}{}
    \tagstructbegin{tag=LI}
    \tagmcbegin{tag=Lbl} - \tagmcend % Character encoding error on use of bullet causing accessibility test to fail
    \tagstructbegin{tag=LBody}\openLBodyContainer
    \global\toggletrue{LIOpen}
}
  
\renewcommand{\labelenumi}{
    \iftoggle{LIOpen}{\closeItem}{}
    \tagstructbegin{tag=LI}
    \tagmcbegin{tag=Lbl} (\Alph*) \tagmcend
    \tagstructbegin{tag=LBody}\openLBodyContainer
    \global\toggletrue{LIOpen}
}

\renewcommand{\labelenumii}{
    \iftoggle{LIOpen}{\closeItem}{}
    \tagstructbegin{tag=LI}
    \tagmcbegin{tag=Lbl} \small{\roman*.} \tagmcend
    \tagstructbegin{tag=LBody}\openLBodyContainer
    \global\toggletrue{LIOpen}
}

%Accessible paragraphs
\newtoggle{ParagraphContainerOpen}
\global\togglefalse{ParagraphContainerOpen}

\newtoggle{RequireParagraphRestore}
\global\togglefalse{RequireParagraphRestore}

\newcommand{\openParagraphContainer}{
  \tagmcbegin{tag=P}
   \global\toggletrue{ParagraphContainerOpen}
}

\newcommand{\closeParagraphContainer}{
  \tagmcend %P
   \global\togglefalse{ParagraphContainerOpen}
}

\let\originalparagraph\paragraph%
\renewcommand{\paragraph}
{
    \@ifstar
    {\originalparagraphWithStar}%
    {\@ifnextchar[%]
        {\originalparagraphWithTwoOption}%
        {\originalparagraphWithOption}%
    }%
}%

\newcommand{\originalparagraphWithStar}[1]%
{ 
    \tagstructbegin{tag=P} \openParagraphContainer #1 \closeParagraphContainer \tagstructend
}
\newcommand{\originalparagraphWithTwoOption}[2]%
{
    \tagstructbegin{tag=P} \openParagraphContainer \originalparagraph[#1]{#2} \closeParagraphContainer \tagstructend
}
\newcommand{\originalparagraphWithOption}[1]%
{
     \tagstructbegin{tag=P} \openParagraphContainer #1 \closeParagraphContainer \tagstructend
}

\let\originalsubparagraph\subparagraph%
\renewcommand{\subparagraph}
{
    \@ifstar
    {\originalsubparagraphWithStar}%
    {\@ifnextchar[%]
        {\originalsubparagraphWithTwoOption}%
        {\originalsubparagraphWithOption}%
    }%
}%

\newcommand{\originalsubparagraphWithStar}[1]%
{ 
    \tagstructbegin{tag=P} \openParagraphContainer \originalsubparagraph*{#1} \closeParagraphContainer \tagstructend
}
\newcommand{\originalsubparagraphWithTwoOption}[2]%
{
    \tagstructbegin{tag=P} \openParagraphContainer \originalsubparagraph[#1]{#2} \closeParagraphContainer \tagstructend
}
\newcommand{\originalsubparagraphWithOption}[1]%
{
     \tagstructbegin{tag=P} \openParagraphContainer \originalsubparagraph{#1} \closeParagraphContainer \tagstructend
}

% Accessible link tagging
\renewcommand{\url}[1]
{
    \iftoggle{ParagraphContainerOpen}{\closeParagraphContainer \global\toggletrue{RequireParagraphRestore}}{}
    \iftoggle{LBodyContainerOpen}{\closeLBodyContainer \global\toggletrue{RequireLBodyRestore}}{}

    \tagstructbegin{tag=Link, actualtext-o=#1, alttext=#1}
    \tagmcbegin{tag=Link}   
    \href{#1}{#1}
    \tagmcend 
    \tagstructend
    
    \iftoggle{RequireParagraphRestore}{\openParagraphContainer \global\togglefalse{RequireParagraphRestore}}{}
    \iftoggle{RequireLBodyRestore}{\openLBodyContainer \global\togglefalse{RequireLBodyRestore}}{}
}

% Character encoding error on use of \texttt{} causing accessibility test to fail
\renewcommand{\texttt}{}

% Custom maketitle command, using tikz for fancy layout
\renewcommand{\maketitle}{%
    \tagstructbegin{tag=Div, title={Document header}}
        \begin{tikzpicture}[remember picture, overlay]
            \node[anchor=north west, xshift=1cm, yshift=-1cm] (banner) at (current page.north west) {
                \tagmcbegin{artifact=background} % Accessibility: ignore this image
                    \includegraphics[width=19cm]{header}
                \tagmcend
            };
            \node[anchor=north east, xshift=-0.5cm, yshift=-0.5cm] at (banner.north east) {
                \parbox[t]{18cm}{\raggedleft\Huge\color{white}{
                    \tagstructbegin{tag=Title}
                        \tagmcbegin{tag=Title, actualtext-o=\@title}
                            \MakeUppercase{\@title}
                        \tagmcend
                    \tagstructend
                }}
            };
            \node[anchor=south east, xshift=-0.5cm, yshift=0.5cm] at (banner.south east) {
                \parbox[t]{18cm}{\raggedleft\color{white}{
                    %Version \@version\\Computing\\\@module
                    \p{Version \@version}\\\p{Computing}\\\p{\@module}
                }}
            };
            \node[anchor=north west] at (banner.south west) {
                \parbox[t]{18cm}{\raggedright{
                    \p{\@author}
                }}
            };
        \end{tikzpicture}
    \tagstructend
    \vspace{4cm}
}

% Section headers
% Code to override these was ``inspired'' by the accessibility package
\let\originalsection\section%
\renewcommand{\section}{%
    \@ifstar{\originalsectionWithStar}%
    {\@ifnextchar[%]
        {\originalsectionWithTwoOption}%
        {\originalsectionWithOption}%
    }%
}%

\newcommand{\originalsectionWithStar}[1]{\originalsection*{\tag{H1}{#1}}}
\newcommand{\originalsectionWithTwoOption}[2]{\originalsection[#1]{\tag{H1}{#2}}}
\newcommand{\originalsectionWithOption}[1]{\originalsection{\tag{H1}{#1}}}

\let\originalsubsection\subsection%
\renewcommand{\subsection}{%
    \@ifstar{\originalsubsectionWithStar}%
    {\@ifnextchar[%]
        {\originalsubsectionWithTwoOption}%
        {\originalsubsectionWithOption}%
    }%
}%

\newcommand{\originalsubsectionWithStar}[1]{\originalsubsection*{\tag{H2}{#1}}}
\newcommand{\originalsubsectionWithTwoOption}[2]{\originalsubsection[#1]{\tag{H2}{#2}}}
\newcommand{\originalsubsectionWithOption}[1]{\originalsubsection{\tag{H2}{#1}}}

\let\originalsubsubsection\subsubsection%
\renewcommand{\subsubsection}{%
    \@ifstar{\originalsubsubsectionWithStar}%
    {\@ifnextchar[%]
        {\originalsubsubsectionWithTwoOption}%
        {\originalsubsubsectionWithOption}%
    }%
}%

\newcommand{\originalsubsubsectionWithStar}[1]{\originalsubsubsection*{\tag{H2}{#1}}}
\newcommand{\originalsubsubsectionWithTwoOption}[2]{\originalsubsubsection[#1]{\tag{H2}{#2}}}
\newcommand{\originalsubsubsectionWithOption}[1]{\originalsubsubsection{\tag{H2}{#1}}}

% Graphics with alt text
\newcommand{\includegraphicsalt}[3][]{%
    \tagstructbegin{tag=Figure, alttext-o={#3}}
        \tagmcbegin{tag=Figure}
            \includegraphics[#1]{#2}
        \tagmcend
    \tagstructend
}

% Inspirational quote in the margin
\newcommand{\marginquoterule}{
\tagmcend \tagstructend
\marginquoteruleb
\tagstructbegin{tag=P}\tagmcbegin{tag=P}
}

\newcommand{\marginquoteruleb}{
{\color{black}\rule{4.5cm}{1pt}}
}

% \NewEnviron{marginquote}{%
%     \begin{tikzpicture}[remember picture, overlay]
%         \node[anchor=west, xshift=1.5cm] at (current page.west) {
%             \parbox[t]{4.5cm}{%
%                 \setlength{\parskip}{1em}%
%                 \marginquoterule\par%
%                 \small\centering\emph{\color{blue!50!black}%
%                     \tag{BlockQuote}{\BODY}%
%                 }\par%
%                 \marginquoterule%
%             }
%         };
%     \end{tikzpicture}
% }

\newcommand{\marginquoteb}[2]{%
    \tagstructbegin{tag=BlockQuote}
        \begin{tikzpicture}[remember picture, overlay]
            \node[anchor=west, xshift=1.5cm] at (current page.west) {
                \parbox[t]{4.5cm}{%
                    \setlength{\parskip}{1em}%
                    \marginquoteruleb\par%
                    \small\centering\em\color{blue!50!black}\p{#1}\par%
                    %\small\centering\emph{\color{blue!50!black}\p{--- #2}}\par%
                    \marginquoteruleb%
                }
            };
        \end{tikzpicture}
    \tagstructend
}

\NewEnviron{marginquote}{\marginquoteb{\BODY}{}}

% Inspirational image in the margin
% First parameter is the image file name, second parameter is the caption
\newcommand{\marginpicture}[3][A decorative picture]{%
    \ifstrequal{#1}{A decorative picture}{\typeout{Accessibility warning: no alt text for marginpicture}}{}
    \tagstructbegin{tag=Div}
    \begin{tikzpicture}[remember picture, overlay]
        \node[anchor=south west, xshift=1.5cm, yshift=1.5cm] at (current page.south west) {
            \parbox[t]{4.5cm}{%
                \tagstructbegin{tag=Figure, alttext=#1}
                \tagmcbegin{tag=Figure}
                \includegraphics[width=4.5cm]{#2}
                \tagmcend
                \tagstructend
                \par
                {\footnotesize \tag{Caption}{#3}}
            }
        };
    \end{tikzpicture}
    \tagstructend
}

% Marking rubric
\newtoggle{CriterionOpen}
\global\togglefalse{CriterionOpen}

\newcommand{\openCriterion}{
   \tagstructbegin{tag=TR}
   \global\toggletrue{CriterionOpen}
}

\newcommand{\closeCriterion}{
  \tagstructend %TR
   \global\togglefalse{CriterionOpen}

}

\newtoggle{GradeOpen}
\global\togglefalse{GradeOpen}

\newcommand{\openGrade}{
   \tagstructbegin{tag=TD}
   \tagmcbegin{tag=TD}
   \global\toggletrue{GradeOpen}
   \hspace{-0.8em} % I don't know what is causing this offset
}

\newcommand{\closeGrade}{
  \tagmcend %TD
  \tagstructend %TD
   \global\togglefalse{GradeOpen}
}

\newenvironment{markingrubric}{%
    \clearpage
    \newgeometry{margin=1cm}
    %\renewcommand{\arraystretch}{1.25}
    \begin{landscape}
        \section*{\@rubrictitle}
        \begingroup\scriptsize
            \p{\@rubrichead}\\
            \tagstructbegin{tag=Table, alttext=\@rubrictitle}
            \arrayrulecolor{gray!40}
            \setlength\arrayrulewidth{1pt}
            \begin{longtable}{p{2.5cm}p{1.5cm}*{6}{p{3.4cm}}}
                \hline\\[0.3em]
                \openCriterion\centering \textbf{\small \tag{TH}{Criterion}} &
                \centering \textbf{\small \tag{TH}{Weight}} &
                \@rubricgrades \closeCriterion \endhead
                 \hline\\[0.5em]
}{
                \iftoggle{GradeOpen}{\closeGrade}{}
                \iftoggle{CriterionOpen}{\closeCriterion}{}
                \tabularnewline
                \hline
            \end{longtable}
            \tagstructend %Table
            \@rubricfoot
        \endgroup
    \end{landscape}
    
}

% Commands inside the marking rubric
% Use firstcriterion for the first criterion, and criterion for subsequent ones
% The difference is that firstcriterion doesn't start a new table row, because \endhead did that already
% TODO: Investigate why \hspace is needed
\newcommand{\firstcriterion}[2]{\strut \openCriterion \hspace{-1.6em} \setlength{\parskip}{0.5em}\raggedright \tag{TD}{#1} & \centering \tag{TD}{#2}}
\newcommand{\criterion}[2]{\iftoggle{GradeOpen}{\closeGrade}{} \iftoggle{CriterionOpen}{\closeCriterion}{} \openCriterion \tabularnewline\setlength{\parskip}{0.8em}\raggedright \hspace{-0.8em} \tag{TD}{#1} & \centering \tag{TD}{#2}}
\newcommand{\grade}{\iftoggle{GradeOpen}{\closeGrade}{} & \openGrade \setlength{\parskip}{0.5em}\raggedright}
\newcommand{\fail}{}
\newcommand{\gradespan}[2]{& \multicolumn{#1}{p{3.4cm * #1 + (\tabcolsep * 2 + \arrayrulewidth) * (#1 - 1)}|}%
    {\setlength{\parskip}{0.5em}\raggedright \tag{TD}{#2}}}

% Modifiers for title, header and footer of the marking rubric
% Note that these must be specified *before* \begin{markingrubric}
\newcommand{\@rubrictitle}{Marking Rubric}
\newcommand{\rubrictitle}[1]{\renewcommand{\@rubrictitle}{#1}}
\newcommand{\@rubrichead}{}
\newcommand{\rubrichead}[1]{\renewcommand{\@rubrichead}{#1}}
\newcommand{\@rubricfoot}{}
\newcommand{\rubricfoot}[1]{\renewcommand{\@rubricfoot}{#1}}

\newcommand{\@rubricgrades}{
	\centering \textbf{\small \tag{TH}{Near Pass}} &
	\centering \textbf{\small \tag{TH}{Adequate}} &
	\centering \textbf{\small \tag{TH}{Competent}} &
	\centering \textbf{\small \tag{TH}{Very Good}} &
	\centering \textbf{\small \tag{TH}{Excellent}} &
	\centering \textbf{\small \tag{TH}{Outstanding}}
}
\newcommand{\rubricyeartwo}{\@rubricgrades}
\newcommand{\rubricyearthree}{\@rubricgrades}

% PDF properties for accessibility
% https://stackoverflow.com/a/3430025
\makeatletter
\AtBeginDocument{
    % Need to set PDF title and author here to make sure they have been defined
    \hypersetup{
        pdftitle = {\@title},
        pdfauthor = {\@author}
    }
    % Open the document structure tag
    \tagstructbegin{tag=Document}
}
\makeatother

\AtEndDocument{
    % Close the document structure tag
    \tagstructend
}
