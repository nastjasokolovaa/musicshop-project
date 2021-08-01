function addToBasket(url) {
    $.ajax(url)
        .then((body, _, resp) => {
            if (resp.status === 200 && body.status === 'ok') {
                alert('Товар добавлен в корзину')
            } else {
                throw resp
            }
        })
        .catch(resp => {
            if (resp.status === 410) {
                alert('Товар закончился')
            } else {
                console.error(resp)
                alert(`Произошла ошибка: ${resp.status}`)
            }
        })

    return false
}
