
$(".reaction").on('click', function(){
    let action = $(this).attr('action');
    let id = $(this).attr('post-id')
    $.ajax({
        method: 'GET',
        url: '/set_reaction/',
        data:{
            'id': id,
            'action': action,
        },
        success: function(response){
            console.log(response);
        }
    })
})
$("[action=1]").on('click', function(){
    $(this).toggleClass('liked')
})

$("[action=2]").on('click', function(){
    $(".comments[post-id='" + $(this).attr('post-id') + "']").toggleClass('hidden');
})

$("[action=3]").on('click', function(){
    $(this).toggleClass('reposted')
})
$("[action=4]").on('click', function(){
    $(this).toggleClass('bookmarked')
})

$('.post-comment').on('click', function(event){
    event.preventDefault();
    let text_area_content = $("textarea[post-id=" + $(this).attr('post-id') + "]").val();
    const user_id = JSON.parse(document.getElementById('user_id').textContent);

    $.ajax({
        method: 'GET',
        url: '/set_comment/',

        data: {
            'id': $(this).attr('post-id'),
            'text': text_area_content,
        },
        success: function (response){
            console.log(response);
        }
    })
})