


document.addEventListener('DOMContentLoaded', function(){
var myLike = document.getElementById("myLike").value


 var btns=document.querySelectorAll('.editbtn')
 for(let btn of btns){
     document.getElementById(btn.id).addEventListener('click',function(){
     edit(btn)
     })
     }
  var likeBtns=document.querySelectorAll('.likebtn')
 for(let btn of likeBtns){
     if( myLike.includes(btn.id)){
     btn.innerText='Unlike'
     }
     document.getElementById(btn.id).addEventListener('click',function(){
     like(btn)

     })
     }



})





function like(btn){
var classes = $('#'+ btn.id).attr('class').split(' ');
var myclass=classes[1]
let likes=$('#likes'+ myclass)
console.log(likes)
var oldlikes=parseInt(likes[0].textContent)
console.log(oldlikes)
let id=myclass
if(btn.innerText==='Like'){
var newlikes=oldlikes++
console.log(newlikes)
likes[0].textContent=`${++newlikes}`
btn.innerText='Unlike'
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
console.log(newlikes)
likes[0].textContent=`${--newlikes}`
btn.innerText='Like'

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












function edit(btn){
var oldText=document.getElementById('edit'+btn.id)
var container=document.querySelector('.edit-container')
console.log(container)
    oldText.contentEditable='true'
    btn.innerText='Save'


    oldText.classList.add("edit")
    btn.addEventListener('click', function(){
    oldText.contentEditable='false'
       btn.innerText='Edit'
       oldText.classList.remove("edit")
       let id=btn.id
       let newText=oldText.innerText
       console.log(btn.id)
       $.ajax({
    url : `/editpost/${id}`,
    type : "POST",
    data : {
        'csrfmiddlewaretoken' : "{{  csrf_token  }}",
        text : newText
    },
    success : function(result) {}
});
    })
}















function likePost(post_id) {
         let text = 'EDITED BITCH!!';

$.ajax({
    url : `/editpost/${post_id}`,
    type : "POST",
    data : {
        'csrfmiddlewaretoken' : "{{  csrf_token  }}",
        text : text
    },
    success : function(result) {}
});


}










