param([Parameter(Mandatory=$true)][string]$OutputDir,[string]$Name)
$ErrorActionPreference='Stop'
$resolved=(Resolve-Path -LiteralPath $OutputDir).Path
if(-not $Name){
 $candidates=@(Get-ChildItem -LiteralPath $resolved -Filter '*.docx')
 if($candidates.Count -ne 1){throw 'Pass -Name when the directory does not contain exactly one DOCX.'}
 $Name=$candidates[0].BaseName
}
$wordWasRunning=($null -ne (Get-Process WINWORD -ErrorAction SilentlyContinue))
$word=New-Object -ComObject Word.Application
$oldBackgrounds=$word.Options.PrintBackgrounds
$word.Visible=$false
$word.DisplayAlerts=0
$doc=$null
try {
 $word.Options.PrintBackgrounds=$true
 $doc=$word.Documents.Open((Join-Path $resolved ($Name+'.docx')),$false,$true)
 $doc.Repaginate()
 $doc.ExportAsFixedFormat((Join-Path $resolved 'DOCX-office.pdf'),17)
 Write-Output ('Word pages: '+$doc.ComputeStatistics(2))
} finally {
 if($doc){try{$doc.Close(0)}catch{}}
 try{$word.Options.PrintBackgrounds=$oldBackgrounds;if(-not $wordWasRunning){$word.Quit()}}catch{}
}
$pptWasRunning=($null -ne (Get-Process POWERPNT -ErrorAction SilentlyContinue))
$ppt=New-Object -ComObject PowerPoint.Application
$pres=$null
try {
 $pres=$ppt.Presentations.Open((Join-Path $resolved ($Name+'.pptx')),$true,$false,$false)
 $pres.SaveAs((Join-Path $resolved 'PPTX-office.pdf'),32)
 Write-Output ('PowerPoint slides: '+$pres.Slides.Count)
} finally {
 if($pres){try{$pres.Close()}catch{}}
 if(-not $pptWasRunning){try{$ppt.Quit()}catch{}}
}
