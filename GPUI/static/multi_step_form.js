/*------------Validation Function-----------------*/
// var count = 0; // To count blank fields.
// function validation(event) {
// var radio_check = document.getElementsByName('gender'); // Fetching radio button by name.
// var input_field = document.getElementsByClassName('text_field'); // Fetching all inputs with same class name text_field and an html tag textarea.
// var text_area = document.getElementsByTagName('textarea');
// // Validating radio button.
// if (radio_check[0].checked == false && radio_check[1].checked == false) {
// var y = 0;
// } else {
// var y = 1;
// }
// // For loop to count blank inputs.
// for (var i = input_field.length; i > count; i--) {
// if (input_field[i - 1].value == '' || text_area.value == '') {
// count = count + 1;
// } else {
// count = 0;
// }
// }
// if (count != 0 || y == 0) {
// alert("*All Fields are mandatory*"); // Notifying validation
// event.preventDefault();
// } else {
// return true;
// }
// }
/*---------------------------------------------------------*/
// Function that executes on click of first next button.
function next_step1() {
document.getElementById("first").style.display = "none";
document.getElementById("second").style.display = "block";
document.getElementById("active2").style.color = "red";
}
// Function that executes on click of first previous button.
function prev_step1() {
document.getElementById("first").style.display = "block";
document.getElementById("second").style.display = "none";
document.getElementById("active1").style.color = "red";
document.getElementById("active2").style.color = "gray";
}
// Function that executes on click of second next button.
function next_step2() {
document.getElementById("second").style.display = "none";
document.getElementById("third").style.display = "block";
document.getElementById("active3").style.color = "red";
}
// Function that executes on click of second previous button.
function prev_step2() {
document.getElementById("third").style.display = "none";
document.getElementById("second").style.display = "block";
document.getElementById("active2").style.color = "red";
document.getElementById("active3").style.color = "gray";
}
// Function that executes on click of third next button.
function next_step3() {
    document.getElementById("third").style.display = "none";
    document.getElementById("forth").style.display = "block";
    document.getElementById("active4").style.color = "red";
    }
    // Function that executes on click of third previous button.
function prev_step3() {
    document.getElementById("forth").style.display = "none";
    document.getElementById("third").style.display = "block";
    document.getElementById("active3").style.color = "red";
    document.getElementById("active4").style.color = "gray";
}

// Activate result tabs based on click

// function policy_wise() {
//     document.getElementById("first").style.display = "block";
//     document.getElementById("second").style.display = "none";
//     document.getElementById("active1").style.color = "red";
//     document.getElementById("active2").style.color = "gray";
// }
// function location_wise() {
//     document.getElementById("first").style.display = "none";
//     document.getElementById("second").style.display = "block";
//     document.getElementById("active2").style.color = "red";
//     document.getElementById("active1").style.color = "gray";
// }

$(document).ready(function(){
    $('ul.resultpages li').click(function(){
        let clickedText = $(this).text();
        if(clickedText == "Policy Wise") {
            document.getElementById("first").style.display = "block";
            document.getElementById("second").style.display = "none";
            document.getElementById("active1").style.color = "red";
            document.getElementById("active2").style.color = "gray";
        }
        else
        {
            document.getElementById("first").style.display = "none";
            document.getElementById("second").style.display = "block";
            document.getElementById("active2").style.color = "red";
            document.getElementById("active1").style.color = "gray";
        }

    });
});
/*
using ajax call to send form data to view for getting response
*/

// $(document).ready(function(){
//     $('#myForm').submit(function (e) {
//         e.preventDefault();
//         //  console.log($(this).serialize());
//         $.ajax({
//             type: 'POST',
//             url: 'save_form_data',
//             data: $(this).serialize(),
//             success: function(response){
//                 console.log(response);
//                 // window.location.href ='success/';

//             },
//             error:function(error){
//                 console.log(error);
//                 // window.location.href ='success/';
//             }

//         });
//     });
// });

/insert and delete rows into calim experiance table/
function claimExprow()  
{  
// console.log('hi');
var x = document.getElementById('claimexptbl');
var new_row = x.rows[1].cloneNode(true);
var len = x.rows.length;
x.appendChild(new_row); 
}  
function claimExpDel()  
{  
    var mytable = document.getElementById("claimexptbl");  
    var rows = mytable.rows.length;  
    for(var i = rows - 1; i > 0; i--)  
    {  
        if(mytable.rows[i].cells[0].children[0].checked)  
        {  
            mytable.deleteRow(i);  
        }  
    }  
}  
/insert and delete rows into location table/
function row()  
{  
// console.log('hi');
var x = document.getElementById('locationtbl');
var new_row = x.rows[2].cloneNode(true);
var len = x.rows.length;
x.appendChild(new_row); 
}  
function del()  
{  
    var mytable = document.getElementById("locationtbl");  
    var rows = mytable.rows.length;  
    for(var i = rows - 1; i > 0; i--)  
    {  
        if(mytable.rows[i].cells[0].children[0].checked)  
        {  
            mytable.deleteRow(i);  
        }  
    }  
}  

// show and hide rows based on header

$(document).ready(function(){
	
	$('.collapsible-header').click(function() {
		$(this).toggleClass('collapsed');
		$(this).next('.collapsible-content').slideToggle();
	});
	
    $('tr.cheader').click(function(){
        $(this).find('span').text(function(_, value){return value=='-'?'+':'-'});
        $(this).prevUntil('tr.cheader').slideToggle(100, function(){
        });
    });
});

function toggleloccolmns() {
    $('.sub-loc-column').toggle();
    $('th.loc-collapsed').text(function(i,text) {
            return text === '+' ? '-' : '+' ;
    });
}
function togglebuildcolmns() {
    $('.sub-build-column').toggle();
    $('th.build-collapsed').text(function(i,text) {
            return text === '+' ? '-' : '+' ;
    });
}