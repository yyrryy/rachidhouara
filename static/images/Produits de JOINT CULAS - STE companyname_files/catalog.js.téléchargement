
const client = $('.clientid');
const tablecmnd = $('.commande-table');
const csrf= $("[name=csrfmiddlewaretoken]").val()


// filter table function
function searchtable() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    // lower the input value
    filter = input.value.toLowerCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[1];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.includes(filter)) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
}

const checkstorage = (id)=>{
    products=JSON.parse(localStorage.getItem('products')) || []
    if(products.includes(id)){
        return true
    }
    return false
}



const savetostorage=(id, ref, n, ctg, qty, pr, tt, img, min)=>{
    // get products from localstorage
    products=JSON.parse(localStorage.getItem('products')) || []
    productsdetails=JSON.parse(localStorage.getItem('productsdetails')) || []
    // add the new product
    let pdct=[ref, n, ctg, qty, pr, tt, img, min, id]
    products.push(id)
    productsdetails.push(pdct)
    // save to localstorage
    localStorage.setItem('products', JSON.stringify(products))
    localStorage.setItem('productsdetails', JSON.stringify(productsdetails))
}




const addcmnd=(name, ctg, ref, qty, pr, id, img, min)=>{
    // checks local storage if the item is already there
    if(!checkstorage(id)){
        sub=(pr*qty).toFixed(2)
        let bigt=parseFloat($('.ttt').text())
        $('.ttt').text((bigt+parseFloat(sub)).toFixed(2))
        // $('.ttt').text(((parseFloat($('.ttt').text()))+sub).toFixed(2))
        savetostorage(id, ref, name, ctg, qty, pr, sub, img, min)
        $('.commanditems').html(parseInt($('.commanditems').html())+1)
        $('.valider').prop('disabled', false)

        // $('.fromclient').prop('disabled', false)
        // tablecmnd.append(`
        // <tr class="cmndholder">
        // <td class="pdctcmnd" ref=${ref} name="${name}">
        //     ${ref}
        // </td>
        // <td class="pdctcmnd" ref=${ref} name="${name}">
        //     ${name}
        // </td>
        // <td class="qtyholder">
        //     <div class="cart-table__quantity input-number"><input readonly class="form-control input-number__input qty" type="number" min="${min}" value="${qty}" price="${pr}" name='qtytosub'><div class="input-number__add"></div><div class="input-number__sub"></div></div>
            
        // </td>
        // <td class="subtotal">
        //     ${sub}
            
        // </td>
        
        // </tr>
        // `)

        // $('.input-number').customNumber();
        // $("input[name=qtytosub]").each((i, el)=>{
        //     $(el).on('change', ()=>{
        //         v=$(el).val()
        //         subt=$(el).attr('price')*v
        //         // find the subtotal cell
        //         $(el).parent().parent().parent().find('.subtotal').text(subt.toFixed(2))
        //         updatetotal()
        //     }
        // )})
        return
    }
    alert('Deja commandée')

}



const close = function() {

    $('body').css({
        'overflow': 'auto',
        'paddingRight': ''
    });
};
const open = function() {

    $('body').css({
        'overflow': 'hidden',
        'paddingRight': ''
    });
};

const updateclients=()=>{
    loading()
    $.ajax({
        url: '/clients',
        type: 'GET',
        
        success: function(data){
            stoploading()
            $('[name=client]').html('<option value="0">---</option>')
            for (i of JSON.parse(data.clients)){
                $('[name=client]').append(`
                <option value="${i.id}">${i.name} (${i.address})</option>
                `)
            }
        },
        error:(err)=>{
            stoploading()
            alert(err)
        }
    })
}


$("#addclientform").submit(function(event) {
    event.preventDefault();

    var formData = $(this).serialize();
    loading()
    $.ajax({
      type: "POST",
      url: "/addclient",
      data: formData,
      success: function(response) {
        stoploading()
        // handle the response from the server
        $('#addclientmodal').modal('hide')
        updateclients()
      }
    });
  });

// handle .addclient click
// const addclientform=(e)=>{
//     e.preventDefault()
//     $.ajax({
//         url: '/addclient',
//         type: 'POST',
//         data: {
//             nom: $('input[name="nom"]').val(),
//             city: $('input[name="city"]').val(),
//             phone: $('input[name="phone"]').val(),
//             csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
//         },
//         success: function(response){
//             $('#addclientmodal').modal('hide')
//             updateclients()
//         }
//     })
// }

// clear commande
const clearcommande=()=>{
    if (confirm('Supprimer la commande')){

        clearstorage()
        $('.valider').prop('disabled', true)
        $('.fromclient').prop('disabled', true)
        $('.total').text('0.00')
        return
    }
    return
}




$('.cmnd').each((i, el)=>{
    $(el).on('click', ()=>{
        // id=$(el).attr('pdct');
        $(el).attr('disabled', true)
        added=$(el).parent.find('.added')
        added.toggleClass('.d-none')
        setTimeout(()=>{
            added.toggleClass('.d-none')
        }, 3000)
        ref=$(el).attr('pdctref')
        name=$(el).attr('pdctname')
        ctg=$(el).attr('pdctcategory')
        pr=$(el).attr('pdctpr')
        id=$(el).attr('pdctid')
        img=$(el).attr('pdctimg')
        min=$(el).attr('pdctmin')
        // get nearest item
        let qty = $(el).parent().find('.input-number > .input-number__input').val()
        // add new row to coommand table
        addcmnd(name, ctg, ref, qty, pr, id, img, min)
        // update total

    })
})

$('[name=category]').on('change',() => {
            loading()
    
            $.ajax({
                method:'Post',
                url:'/filters',
                data:{
                csrfmiddlewaretoken:csrf,
                category:$('select[name=category]').val()=='0'?null:+$('select[name=category]').val(),
                brand:$('input[name="brand"]').val()=='0'?null:$('input[name="brand"]').val(),
                model:$('input[name="model"]').val()=='0'?null:$('input[name="model"]').val(),
                mark:$('input[name="mark"]').val()=='0'?null:$('input[name="mark"]').val()
            },
                success:(data)=>{
                    stoploading()
                    $('.prdctslist').html(data.data)
                    $('.input-number').customNumber();
                    $('.cmnd').each((i, el)=>{
                        $(el).on('click', ()=>{
                            
                            // id=$(el).attr('pdct');
                            $(el).attr('disabled', true)
                            ref=$(el).attr('pdctref')
                            name=$(el).attr('pdctname')
                            pr=$(el).attr('pdctpr')
                            id=$(el).attr('pdctid')
                            // get nearest item
                            let qty = $(el).parent().find('.input-number > .input-number__input').val()
                            // add new row to coommand table
                            addcmnd(name, ref, qty, pr, id)
                            // update total

                        })
                    })
                },
                Error:(error)=>{
                    stoploading()
                    alert('error')
                }
    
            })
    
    
})

$('.valider').on('click', ()=>{
    loading('verification')
    //
    if (client.val()==0 || $('[name="modpymnt"]').val()==0 || $('[name="modlvrsn"]').val()==0){
        stoploading()
        alert('Veuillez choisir un mode de payement ou de livraison')
        $('.modes').addClass('border-danger')
        return
    }
    validercmnd(client.val())
    // client.val()==0?stoploading():validercmnd(client.val())
    // clientid=client.val()
    // if(clientid=='0'){
    //     $('.clienterr').removeClass('d-none').addClass('d-block')
    //     return
    // }
    // else{
    //     loading()
    //     $('.valider').prop('disabled', true)
    //     $('.fromclient').prop('disabled', true)
    //     $('.clienterr').removeClass('d-block').addClass('d-none')
    //     validercmnd(clientid)
    //     clearstorage()
    //     stoploading()
    //     window.location.reload()
    // }

})

$('.fromclient').on('click', ()=>{
    loading('verification')
    
})

// hide commande
$('.hidecommande').on('click', ()=>{
    $('.cartholder').css({
        'right':'-500rem'
    })
    $('body').removeClass('overflow-hidden position-fixed')
})

// show commande
$('.showcommande').on('click', ()=>{
    $('.cartholder').css({
        'right':'0'
    })
    $('body').addClass('overflow-hidden position-fixed')
})



//A little delay
let typingTimer;               
let typeInterval = 500;
let pdctscards = document.querySelectorAll('.products-list__item')
  function pdctsliveSearch(e) {
    //Use innerText if all contents are visible
    //Use textContent for including hidden elements
    for (var i = 0; i < pdctscards.length; i++) {
        if(pdctscards[i].textContent.toLowerCase()
                .includes(e.target.value.toLowerCase())) {
                    pdctscards[i].classList.remove("d-none");
        } else {
            pdctscards[i].classList.add("d-none");
        }
    }
  }
  let pdctssearchInput = document.getElementById('searchbox');

  pdctssearchInput.addEventListener('keyup', (e) => {
      console.log('rr')
      clearTimeout(typingTimer);
      typingTimer = setTimeout(pdctsliveSearch(e), typeInterval);
  });


// fixed cart
$(window).scroll(function() {
    // if ($(this).scrollTop() > 50) {
    //     // $('.cartdd').addClass('fixed-topright')
    //     $('.categorytitle').addClass('fixed-topleft')
    // } else {
    //     // $('.cartdd').removeClass('fixed-topright')
    //     $('.categorytitle').removeClass('fixed-topleft')
    // }
})
