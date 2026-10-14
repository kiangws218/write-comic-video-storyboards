$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$spec=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'text.json') -Raw | ConvertFrom-Json
$invariant=[Globalization.CultureInfo]::InvariantCulture
function N([single]$v){ return $v.ToString('0.###',$invariant) }
$result=@{}
foreach($entry in $spec.PSObject.Properties){
 $style=[Drawing.FontStyle]::Regular
 $familyName=switch($entry.Name){ 'heavy' {$style=[Drawing.FontStyle]::Bold;'Microsoft YaHei'} 'body' {'SimSun'} 'note' {'KaiTi'} 'latin' {$style=[Drawing.FontStyle]::Bold;'Arial'} }
 $family=New-Object Drawing.FontFamily($familyName)
 $result[$entry.Name]=@{}
 foreach($text in $entry.Value){
  $p=New-Object Drawing.Drawing2D.GraphicsPath
  $p.AddString($text,$family,[int]$style,100,[Drawing.PointF]::new(0,0),[Drawing.StringFormat]::GenericTypographic)
  $bounds=$p.GetBounds();$points=$p.PathPoints;$types=$p.PathTypes;$sb=New-Object Text.StringBuilder
  for($i=0;$i -lt $points.Length;$i++){
   $kind=$types[$i] -band 7
   if($kind -eq 0){[void]$sb.Append('M'+(N $points[$i].X)+','+(N $points[$i].Y)+' ')}
   elseif($kind -eq 1){[void]$sb.Append('L'+(N $points[$i].X)+','+(N $points[$i].Y)+' ')}
   elseif($kind -eq 3){[void]$sb.Append('C'+(N $points[$i].X)+','+(N $points[$i].Y)+' '+(N $points[$i+1].X)+','+(N $points[$i+1].Y)+' '+(N $points[$i+2].X)+','+(N $points[$i+2].Y)+' ');$i+=2}
   if($types[$i] -band 128){[void]$sb.Append('Z')}
  }
  $result[$entry.Name][$text]=@{d=$sb.ToString();x=$bounds.X;y=$bounds.Y;w=$bounds.Width;h=$bounds.Height}
  $p.Dispose()
 }
 $family.Dispose()
}
$result | ConvertTo-Json -Depth 6 -Compress | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'text-outlines.json') -Encoding utf8
Write-Output 'Portable vector text outlines generated'
