function deleteHol(holId){
    fetch('/delete-hol', {
        method: 'POST',
        body: JSON.stringify({ holId: holId })
    }).then((_res)=>{
        window.location.href="/";
    })
}