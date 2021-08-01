$(document).ready(() => {
    $('.basket_list').on('click', 'input[type="number"]', () => {
        const quantityEl = event.target
        $.ajax({
            url: `/basket/edit/${quantityEl.name}/${quantityEl.value}/`,
            success: function (data) {
                console.log(data)
                $('.basket_list').html(data.basket_list)
                $('#basket_cost').html(data.total_cost)
                $('#basket_quantity').html(data.total_quantity)
            },
        })
        event.preventDefault()
    })
})
