
# $header=@{
# referer= "https://conjugator.reverso.net/"
# "sec-ch-ua" = '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"'
# "sec-ch-ua-mobile" = "?0"
# "sec-ch-ua-platform" = "macOS"
# "user-agent" = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
# }
import-module HTMLAgilityPack
$uri =  "https://conjugator.reverso.net/conjugation-german-verb-fallen.html"
$response = invoke-webrequest -UserAgent "EventParser PowerShell/7.3.4" -Method GET $uri
$response.Content>content.html
$doc = new-object HTMLAgilityPack.HtmlDocument   
$doc.Load("content.html")


$root = $doc.DocumentNode   
$rows = $root.descendants("div")              

#$htmlContent = $rows|where-object {$_.xpath -eq "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[1]"}
$htmlContent = $rows|where-object {$_.xpath -eq "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/div[1]/div[4]/div[2]/div[1]/div[1]]"}
$htmlDoc = New-Object HtmlAgilityPack.HtmlDocument




# Access the elements
$verbs = $htmlDoc.DocumentNode.SelectNodes("//ul[@class='wrap-verbs-listing']/li")

$title = $htmlDoc.DocumentNode.SelectNodes("//p")
# Display the verbs
write-output $title.innerText
write-output "---------------"
foreach ($verb in $verbs) {
    $subject = $verb.SelectSingleNode("i[@class='graytxt']").InnerText
    $conjugation = $verb.SelectSingleNode("i[@class='verbtxt']").InnerText
    Write-Output "$conjugation"
}