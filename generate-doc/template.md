$if(titleblock)$
$titleblock$

$endif$
$for(header-includes)$
$header-includes$

$endfor$
$for(include-before)$
$include-before$

$endfor$
$if(toc)$
* This will become a table of contents (this text will be scraped).
{:toc}

$endif$
$body$
$for(include-after)$

$include-after$
$endfor$
