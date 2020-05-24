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
\tagpdfsetup{activate-all=true, interwordspace=true}

% Make enumerate / itemize lists more closely spaced
\usepackage{enumitem}
\setlist{nosep}

% Fix for pound sterling sign http://tex.stackexchange.com/a/17858
\usepackage[T1]{fontenc} 

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

\iftoggle{LIOpen}{\closeItem}{}

\newcommand{\closeItem}{
  \tagmcend\tagstructend %LBody
  \tagmcend\tagstructend %LI
   \global\togglefalse{LIOpen}
}

  %
  \let\originalenumerate\enumerate%
  \let\originalendenumerate\endenumerate%
  \renewenvironment{enumerate}%
    {
      \setcounter{NestedEnumDepth}{\value{NestedEnumDepth}+1}
      \ifnumcomp{\value{NestedEnumDepth}}{=}{1}{\tagstructbegin{tag=L}\tagmcbegin{tag=L}}{}
      \originalenumerate
    }{
     \originalendenumerate 
     \iftoggle{LIOpen}{\closeItem}{}
     \ifnumcomp{\value{NestedEnumDepth}}{=}{1}{\tagmcend  \tagstructend}{}
     \setcounter{NestedEnumDepth}{\value{NestedEnumDepth}-1}
     }%

  
    %
  \let\originalitemize\itemize%
  \let\originalenditemize\enditemize%
  \renewenvironment{itemize}%
    {
    \iftoggle{LIOpen}{\closeItem}{}
    \tagstructbegin{tag=L}\tagmcbegin{tag=L}
    \originalitemize
    }{
    \originalenditemize 
    \iftoggle{LIOpen}{\closeItem}{}
    \tagmcend  \tagstructend}%
  %

\let\originaltheenumi\theenumi%
\renewcommand{\theenumi}{
    \iftoggle{LIOpen}{\closeItem}
    \originaltheenumi    
}

\renewcommand{\labelitemi}{
    \iftoggle{LIOpen}{\closeItem}{}
    \tagstructbegin{tag=LI}\tagmcbegin{tag=LI} 
    \tagstructbegin{tag=Lbl}\tagmcbegin{tag=Lbl} - \tagmcend\tagstructend
    \tagstructbegin{tag=LBody}\tagmcbegin{tag=LBody}
    \global\toggletrue{LIOpen}
}
  
\renewcommand{\labelenumi}{
    \iftoggle{LIOpen}{\closeItem}{}
    \tagstructbegin{tag=LI}\tagmcbegin{tag=LI} 
    \tagstructbegin{tag=Lbl}\tagmcbegin{tag=Lbl} (\Alph*) \tagmcend\tagstructend
    \tagstructbegin{tag=LBody}\tagmcbegin{tag=LBody}
    \global\toggletrue{LIOpen}
}

\renewcommand{\labelenumii}{
    \iftoggle{LIOpen}{\closeItem}{}
    \tagstructbegin{tag=LI}\tagmcbegin{tag=LI} 
    \tagstructbegin{tag=Lbl}\tagmcbegin{tag=Lbl} \roman*. \tagmcend\tagstructend
    \tagstructbegin{tag=LBody}\tagmcbegin{tag=LBody}
    \global\toggletrue{LIOpen}
}

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
                    \tagstructbegin{tag=H1}
                        \tagmcbegin{tag=H1, actualtext-o=\@title}
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
                \parbox[t]{18cm}{\raggedright\color{gray}{
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

\newcommand{\originalsectionWithStar}[1]{\originalsection*{\tag{H2}{#1}}}
\newcommand{\originalsectionWithTwoOption}[2]{\originalsection[#1]{\tag{H2}{#2}}}
\newcommand{\originalsectionWithOption}[1]{\originalsection{\tag{H2}{#1}}}

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
\newcommand{\marginquoterule}{{\color{black}\rule{4.5cm}{1pt}}}

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
                    \marginquoterule\par%
                    \small\centering\em\color{blue!50!black}\p{#1}\par%
                    %\small\centering\emph{\color{blue!50!black}\p{--- #2}}\par%
                    \marginquoterule%
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
                {\footnotesize \tag{P}{#3}}
            }
        };
    \end{tikzpicture}
    \tagstructend
}

% Marking rubric
\newenvironment{markingrubric}{%
    \clearpage
    \newgeometry{margin=1cm}
    \begin{landscape}
        \section*{\@rubrictitle}
        \begingroup\scriptsize
            \setlength{\extrarowheight}{2pt}
            \@rubrichead
            \begin{longtable}{|p{2.5cm}|p{1.5cm}|*{6}{p{3.4cm}|}}
                \hline
                \centering \textbf{\small Criterion} &
                \centering \textbf{\small Weight} &
                \@rubricgrades \endhead\hline
}{
                \tabularnewline\hline
            \end{longtable}
            \@rubricfoot
        \endgroup
    \end{landscape}
}

% Commands inside the marking rubric
% Use firstcriterion for the first criterion, and criterion for subsequent ones
% The difference is that firstcriterion doesn't start a new table row, because \endhead did that already
\newcommand{\firstcriterion}[2]{\setlength{\parskip}{0.5em}\raggedright #1 & \centering #2}
\newcommand{\criterion}[2]{\tabularnewline\hline\setlength{\parskip}{0.5em}\raggedright #1 & \centering #2}
\newcommand{\grade}{ & \setlength{\parskip}{0.5em}\raggedright}
\newcommand{\fail}{\cellcolor{gray!50}}
\newcommand{\gradespan}[2]{& \multicolumn{#1}{p{3.4cm * #1 + (\tabcolsep * 2 + \arrayrulewidth) * (#1 - 1)}|}%
    {\setlength{\parskip}{0.5em}\raggedright #2}}

% Modifiers for title, header and footer of the marking rubric
% Note that these must be specified *before* \begin{markingrubric}
\newcommand{\@rubrictitle}{Marking Rubric}
\newcommand{\rubrictitle}[1]{\renewcommand{\@rubrictitle}{#1}}
\newcommand{\@rubrichead}{}
\newcommand{\rubrichead}[1]{\renewcommand{\@rubrichead}{#1}}
\newcommand{\@rubricfoot}{}
\newcommand{\rubricfoot}[1]{\renewcommand{\@rubricfoot}{#1}}

\newcommand{\@rubricgrades}{
	\centering \cellcolor{gray!50} \textbf{\small Refer for Resubmission} &
	\centering \textbf{\small Adequate} &
	\centering \textbf{\small Competent} &
	\centering \textbf{\small Very Good} &
	\centering \textbf{\small Excellent} &
	\centering \textbf{\small Outstanding}
}
\newcommand{\rubricyeartwo}{\renewcommand{\@rubricgrades}{
	\centering \cellcolor{gray!50} \textbf{\small Refer for Resubmission} &
	\centering \textbf{\small Adequate} &
	\centering \textbf{\small Competent} &
	\centering \textbf{\small Very Good} &
	\centering \textbf{\small Excellent} &
	\centering \textbf{\small Outstanding}
}}
\newcommand{\rubricyearthree}{\renewcommand{\@rubricgrades}{
	\centering \cellcolor{gray!50} \textbf{\small Refer for Resubmission} &
	\centering \textbf{\small Adequate} &
	\centering \textbf{\small Competent} &
	\centering \textbf{\small Very Good} &
	\centering \textbf{\small Excellent} &
	\centering \textbf{\small Outstanding}
}}

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
