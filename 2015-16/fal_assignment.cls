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

% Allow document version to be specified, e.g. \version{1.1} in the preamble
% Defaults to 1.0 if not specified
\newcommand{\@version}{1.0}
\newcommand{\version}[1]{\renewcommand{\@version}{#1}}

% Custom maketitle command, using tikz for fancy layout
\renewcommand{\maketitle}{%
    \begin{tikzpicture}[remember picture, overlay]
        \node[anchor=north west, xshift=1cm, yshift=-1cm] (banner) at (current page.north west) {
            \includegraphics[width=19cm]{header}
        };
        \node[anchor=north east, xshift=-0.5cm, yshift=-0.5cm] at (banner.north east) {
            \parbox[t]{18cm}{\raggedleft\Huge\color{white}{\MakeUppercase{\@title}}}
        };
        \node[anchor=south east, xshift=-0.5cm, yshift=0.5cm] at (banner.south east) {
            \parbox[t]{18cm}{\raggedleft\color{white}{Version \@version\\BSc Computing for Games}}
        };
        \node[anchor=north west] at (banner.south west) {
            \parbox[t]{18cm}{\raggedright\color{gray}{\@author}}
        };
    \end{tikzpicture}
    \vspace{4cm}
}

% Inspirational quote in the margin
\newcommand{\marginquoterule}{{\color{black}\rule{4.5cm}{1pt}}}

\NewEnviron{marginquote}{%
    \begin{tikzpicture}[remember picture, overlay]
        \node[anchor=west, xshift=1.5cm] at (current page.west) {
            \parbox[t]{4.5cm}{%
                \setlength{\parskip}{1em}%
                \marginquoterule\par%
                \small\centering\emph{\color{blue!50!black}\BODY}\par%
                \marginquoterule%
            }
        };
    \end{tikzpicture}
}

% Inspirational image in the margin
% First parameter is the image file name, second parameter is the caption
\newcommand{\marginpicture}[2]{%
    \begin{tikzpicture}[remember picture, overlay]
        \node[anchor=south west, xshift=1.5cm, yshift=1.5cm] at (current page.south west) {
            \parbox[t]{4.5cm}{%
                \includegraphics[width=4.5cm]{#1}\par
                {\footnotesize #2}
            }
        };
    \end{tikzpicture}
}

% Marking rubric
\newenvironment{markingrubric}{%
    \clearpage
    \newgeometry{margin=1cm}
    \begin{landscape}
        \section*{Marking Rubric}
        \begingroup\scriptsize
            \setlength{\extrarowheight}{2pt}
            \begin{longtable}{|p{2.5cm}|p{1.5cm}|*{6}{p{3.4cm}|}}
                \hline
                \centering \textbf{\small Criterion} &
                \centering \textbf{\small Weight} &
                \centering \cellcolor{gray!50} \textbf{\small F (0 -- 39)} &
                \centering \textbf{\small D (40 -- 49)} &
                \centering \textbf{\small C (50 -- 59)} &
                \centering \textbf{\small B (60 -- 69)} &
                \centering \textbf{\small A (70 -- 79)} &
                \centering \textbf{\small A$^*$ (80 -- 100)} \endhead\hline
}{
                \tabularnewline\hline
            \end{longtable}
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
