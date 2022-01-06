
document.addEventListener('DOMContentLoaded', function(){
document.getElementById('button').addEventListener('click', function(){
console.log('clicked')
condition='new'
fetch(`/likedposts/18`, {
  method: 'POST',
  body: JSON.stringify({
      liked: true
  })
})



})

}
)





//fetch(`/likedposts/18`, {
 // method: 'PUT',
 // body: JSON.stringify({
  //    liked: true
 // })
//})


  //     $.ajax({
//    url : `/likedposts/18`,
 //   type : "POST",
 //   data : {
   //     'csrfmiddlewaretoken' : "{{  csrf_token  }}",
   //     liked : condition
   // },
  //  success : function() {

//console.log("Success msg");
   // }




//});



 function like(btn){
var classes = $('#'+ btn.id).attr('class').split(' ');
var myclass=classes[1]
let likes=$('#likes'+ myclass)
console.log(likes)
var oldlikes=parseInt(likes[0].textContent)
let id=myclass
//var myLike = document.getElementById("myLike").value
//var myUnlike=document.getElementById("myUnlike").value
//var like_list = document.getElementById("likecount").value
//var unlike_list=document.getElementById("unlikecount").value
var like_btn=document.getElementById("likebtn"+id)
var unlike_btn=document.getElementById("unlikebtn"+id)
console.log(unlike_btn)
 if(btn.innerText==='Like'){
var newlikes=oldlikes++
likes[0].textContent=`${++newlikes}`
btn.style.display='none'
//unlike_btn.style.display='block'

     $.ajax({
    url : `/likedposts/${id}`,
    type : "POST",
    data : {
        'csrfmiddlewaretoken' : "{{  csrf_token  }}",
        liked : 'True',
        unliked: 'False'
    },
    success : function(result) {}
});

}else if(btn.innerText==='Unlike'){
var newlikes=oldlikes--
likes[0].textContent=`${--newlikes}`
btn.style.display='none'
//like_btn.style.display='block'
   $.ajax({
    url : `/likedposts/${id}`,
    type : "POST",
    data : {
        'csrfmiddlewaretoken' : "{{  csrf_token  }}",
        liked : 'False',
        unliked: 'True'
    },
    success : function(result) {}
});
}

//var myLikes=parseInt(myLike)-parseInt(myUnlike)
//console.log(myLikes)
     $.ajax({
    url : `/likes/${id}`,
    type : "POST",
    data : {
        'csrfmiddlewaretoken' : "{{  csrf_token  }}",
        likes : newlikes
    },
    success : function(result) {}
});

 }