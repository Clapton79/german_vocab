# Load the HtmlAgilityPack module
Import-Module HtmlAgilityPack

# Load the HTML content
$htmlContent = @"
<p>Präsens</p>
<ul class="wrap-verbs-listing">
    <li><i class="graytxt">ich </i><i class="verbtxt">falle</i></li>
    <li><i class="graytxt">du </i><i class="verbtxt">fällst</i></li>
    <li><i class="graytxt">er/sie/es </i><i class="verbtxt">fällt</i></li>
    <li><i class="graytxt">wir </i><i class="verbtxt">fallen</i></li>
    <li><i class="graytxt">ihr </i><i class="verbtxt">fallt</i></li>
    <li><i class="graytxt">Sie </i><i class="verbtxt">fallen</i></li>
</ul>
"@

# Parse the HTML content
$htmlDoc = New-Object HtmlAgilityPack.HtmlDocument
$htmlDoc.LoadHtml($htmlContent)

# Access the elements
$verbs = $htmlDoc.DocumentNode.SelectNodes("//ul[@class='wrap-verbs-listing']/li")

# Display the verbs
foreach ($verb in $verbs) {
    $subject = $verb.SelectSingleNode("i[@class='graytxt']").InnerText
    $conjugation = $verb.SelectSingleNode("i[@class='verbtxt']").InnerText
    Write-Output "$subject $conjugation"
}
