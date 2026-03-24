// $('.clientname').val(localStorage.getItem('clientname'))
// $('.clientphone').val(localStorage.getItem('clientphone'))
// $('.clientaddress').val(localStorage.getItem('clientaddress'))
loading()
const updatetotal=()=>{
  t=0
  $('.subtotal').each((i, el)=>{
      t+=parseFloat($(el).text())
  })
  $('.total').text(t.toFixed(2))
  if ($('[name="modpymnt"]').val()=='espece'){
    $('.totalremise').text((t.toFixed(2)*0.95).toFixed(2))
  }else{
    $('.totalremise').text(t.toFixed(2))
  }
  $('.ttt').text(t.toFixed(2))
}


const clearstorage =()=>{
  // clear localstorage
  localStorage.removeItem('products')
  localStorage.removeItem('productsdetails')
  // clear table
  $('.cart-table__body').empty()
  //$('.prdctslist').empty()
  $('.commanditems').text(0)
  updatetotal()
}

const validercmnd=(clientid)=>{
  $('.remise').removeClass('d-none')
  holder=$('.cmndholder')
  // commande=[]
  // holder.each((i, el)=>{
  //     ref=$(el).attr('ref')
  //     id=$(el).attr('id')
  //     n=$(el).attr('n')
  //     qty=$(el).find('.qtyholder .input-number > .qty').val()
  //     cmd=ref+':'+n+':'+qty+':'+id
  //     commande.push(cmd)
  // })
  
  $.ajax({
      url: '/commande',   
      type: 'POST',
      data: {
          'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
          //'commande': commande,
          'clientid':clientid,
          //'total':parseFloat($('.total').text()),
          'modpymnt':$('[name="modpymnt"]').val(),
          'modlvrsn':$('[name="modlvrsn"]').val(),
          'isclient':$('[name="isclient"]').val(),
          'clientname':$('.clientname').val(),
          'clientphone':$('.clientphone').val(),
          'clientaddress':$('.clientaddress').val(),
          'totalremise':parseFloat($('.totalremise').text())
      },

      success: function(data){
        stoploading()
          $('select').val(0)
          $('.modes').removeClass('border-danger')
          $('.cmndholder').remove()
          clearstorage()
          $('.valider').prop('disabled', true)
          $('.fromclient').prop('disabled', true)
          alertify.success('Commande envoyé')
          // go to thank you 
          location.reload()
          // window.location.href='/salsemanorders/'+data.id
          // window.location.href='/catalog'
      },
      error:(err)=>{
          stoploading()
          alertify.error(err)
      }
  })
}
//get items from local storage
// const loadpdcts=()=>{
//   products=JSON.parse(localStorage.getItem('productsdetails'))
//   $('.loadingcartitems').addClass('d-none')
//   if (products && products.length){
//       $('.valider').prop('disabled', false)
//       $('.fromclient').prop('disabled', false)
//       ttt=0
//       for (i of products){
//           let [ref, n, ctg, qty, pr, tt, img, min, id]=i
//           ttt+=parseFloat(tt)

//           $('.cart-table__body').append(`
//           <tr class="cart-table__row cmndholder" ref="${ref}" n="${n}" id="${id}">
          
//           <td class="cart-table__column cart-table__column--product">
//             <a src="${img}" data-toggle="modal" data-target="#imagedisplaymodal" class="imagedisplaybtn" imgsrc="${img}">${ref.toUpperCase()}</a>
//           </td>
//           <td class="cart-table__column cart-table__column--product">
//             <strong>${n.toUpperCase()}</strong>
//           </td>
//           <td class="cart-table__column cart-table__column--price" data-title="Price">
//           <small class="priceholder" price=${pr}>${pr} NET</small>
//           </td>
//           <td class="cart-table__column cart-table__column--quantity qtyholder" data-title="Quantity">
//             <div class="cart-table__quantity input-number">
//               <input readonly class="form-control input-number__input qty" type="number" min="${min?min:1}" value="${qty}" price=${pr} name="qtytosub">
//               <div class="input-number__add"></div>
//               <div class="input-number__sub"></div>
//             </div>
//           </td>
//           <td class="cart-table__column cart-table__column--total subtotal" data-title="Total">
//             <small>${tt} NET</small>
//           </td>
//           <td class="cart-table__column cart-table__column--remove">
//             <button type="button" class="cart-table__remove btn btn-sm btn-icon btn-muted" id="${id}">
//               <svg width="12" height="12">
//                 <path d="M10.8,10.8L10.8,10.8c-0.4,0.4-1,0.4-1.4,0L6,7.4l-3.4,3.4c-0.4,0.4-1,0.4-1.4,0l0,0c-0.4-0.4-0.4-1,0-1.4L4.6,6L1.2,2.6
// c-0.4-0.4-0.4-1,0-1.4l0,0c0.4-0.4,1-0.4,1.4,0L6,4.6l3.4-3.4c0.4-0.4,1-0.4,1.4,0l0,0c0.4,0.4,0.4,1,0,1.4L7.4,6l3.4,3.4
// C11.2,9.8,11.2,10.4,10.8,10.8z"></path>
//               </svg>
//             </button>
//           </td>
//         </tr>
//           `)
//           $('.input-number').customNumber();
//           $("input[name=qtytosub]").each((i, el)=>{
//               $(el).on('change', ()=>{
//                   v=$(el).val()
//                   price=parseFloat($(el).parent().parent().parent().find('.priceholder').text())
//                   subt=price*v
//                   // find the subtotal cell
//                   $(el).parent().parent().parent().find('.subtotal').text(subt.toFixed(2))
//                   updatetotal()
//               }
//           )})
//       }
//       $('.ttt').text(ttt.toFixed(2))
//       $('.total').text(ttt.toFixed(2))
//       return
//   }
// }

$(document).ready(function () {
    
    $('.createclient').on('click', ()=>{
      var isAnyEmpty = $('.notempty').filter(function() { return $(this).val() == ''; }).length > 0;
      if (isAnyEmpty){
        let emptyInputs = $('input.notempty').filter(function() {
          return !this.value.trim();
        });
        
        // Add a red border to all empty input elements
        emptyInputs.css('border', '1px solid red');
        $('input.notempty').not(emptyInputs).css('border', '');
  
      }else{
        loading('client')
        $.ajax({
          type: "POST",
          url: "/addclient",
          data: {
            'name':$('.clientname').val(),
            'phone':$('.clientphone').val(),
            'address':$('.clientaddress').val(),
            'city':$('.clientcity').val(),
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
          },
          success: function (data) {
            stoploading()
            $('.clientid').html(data.options)
            $('input.notempty').val('')
            $('#collapseOne').collapse('hide')
          }
        });
      }
    })

    // valider click
    $('.valider').on('click', ()=>{
        //
        if ($('[name="modpymnt"]').val()==0 || $('[name="modlvrsn"]').val()==0 || $('.clientid').val()==0){
            stoploading()

            let emptySelects = $('select.modes').filter(function() {
              return this.value==0
            });
            // Add a red border to all empty select elements
            emptySelects.addClass('is-invalid');
            
            // Remove the red border from non-empty select elements
            $('select.modes').not(emptySelects).removeClass('is-invalid');
            
            
            return
        }
        // let clientname=$('.clientname').val()
        // let clientaddress=$('.clientaddress').val()
        // let clientphone=$('.clientphone').val()
        // localStorage.setItem('clientname', clientname)
        // localStorage.setItem('clientaddress', clientaddress)
        // localStorage.setItem('clientphone', clientphone)
        alertify.confirm('Valider la commande ?', ()=>{
          clientid=$('.clientid').val()
          loading()
          validercmnd(clientid)
        }, ()=>{

        })
        
    })

    
    
    //$('.input-number').customNumber();
    


    //loadpdcts()
    stoploading()
    // cart delete item
    $('.cart-table__remove').click(function () {
      if (confirm("Supprimer l'article ?")){
        $(this).closest('tr').remove();
        updatetotal()
        // remove from local storage
        products=JSON.parse(localStorage.getItem('products'))
        id=$(this).attr('id')
        // using splice
        products.splice(products.indexOf(id), 1)
        localStorage.setItem('products', JSON.stringify(products))
        // remove from local storage
        productsdetails=JSON.parse(localStorage.getItem('productsdetails'))
        productsdetails.splice(productsdetails.indexOf(id), 1)
        localStorage.setItem('productsdetails', JSON.stringify(productsdetails))
        $('.commanditems').text(products.length)
        // check if cart is empty
        if (products.length==0){
            $('.valider').prop('disabled', true)
        }


      }
    });

    // handle 5% rem
    $('[name="modpymnt"]').on('change', ()=>{
        // if($('[name="modpymnt"]').val()=='espece'){
        //   // $('.priceholder').each((i, el)=>{
        //   //   $(el).text((parseFloat($(el).text())*0.95).toFixed(2))
        //   // })
        //   // $('.subtotal').each((i, el)=>{
        //   //   // animate the update of the total
        //   //   price=parseFloat($(el).parent().parent().find('.priceholder').text())
        //   //   qty=parseFloat($(el).parent().find('.qty').val())
        //   //   $(el).text(parseFloat(price*qty).toFixed(2))
            
            
        //   // })
        //   // updatetotal()
        //   $('.remise').removeClass('d-none')
        //   let total=parseFloat($('.total').text())
        //   let remiseamount=total*0.05
        //   let afterremise=total-remiseamount
        //   $('.totalremise').text(afterremise.toFixed(2))
        // }
        // else{
          
        //   $('.remise').addClass('d-none')
        //   // $("input[name=qtytosub]").each((i, el)=>{
            
        //   //       v=$(el).val()
        //   //       subt=$(el).attr('price')*v
        //   //       // find the subtotal cell
        //   //       subholder=$(el).parent().parent().parent().find('.subtotal')
        //   //       subholder.text(subt.toFixed(2))
        //   //     })
        //   //     $('.priceholder').each((i, el)=>{
        //   //       $(el).text($(el).attr('price'))
        //   //     })
        //   //     updatetotal()
        // }

    })
  });