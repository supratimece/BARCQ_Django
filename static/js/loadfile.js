/*
** Function to load JSON and populate the frontend with respective circuit
*/

function LoadJson2(data2){
	
	try{
		var mydataExtended = JSON.parse(data2);
	}
	catch(e){
		var mydataExtended = data2;
	}
	//var mydataExtended = data2;
	var gatesdata = mydataExtended.instructions;
	//console.log(gatesdata);
	var numOfGates=gatesdata.length;
	for(var gateIndex=0; gateIndex<parseInt(numOfGates); gateIndex++){
		var gateName = gatesdata[gateIndex].name;
		var rowid=gatesdata[gateIndex].rowid;
		var colid=gatesdata[gateIndex].columnid;
		var parent="row"+rowid+"col"+colid+"div";
		CloneIt(gateName,parent);
		rowIds.push(rowid);
        colIds.push(colid);
        ModifyParentDiv($("#"+parent));
	}
}



function loadFile() {
   // $("#fileLoader").click();
var input = document.createElement('input');
input.type = 'file';
input.onchange = e => { 

   // getting a hold of the file reference
   var file = e.target.files[0]; 

   // setting up the reader
   var reader = new FileReader();
   reader.readAsText(file,'UTF-8');

   // here we tell the reader what to do when it's done reading...
   reader.onload = readerEvent => {
      var content = readerEvent.target.result; // this is the content!
      console.log( content );
       LoadJson2(content);
   }

}
input.click();
}