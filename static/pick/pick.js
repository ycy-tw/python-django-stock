const conditionsList = document.querySelector(".conditions");
let addButton = conditionsList.querySelectorAll("button");

for (let i = 0; i < addButton.length; i++) {
    addButton[i].setAttribute("onclick", "addCondition(this)");
}


// add condition
function addCondition(element){

    var firmAttr = element.parentNode.querySelector("span").textContent;
    var choicesList = document.querySelector(".user-choices");
    var haveMatched = true;

    let alreadyHave = choicesList.querySelectorAll("div");
    if (alreadyHave.length < 5) {
        switch(firmAttr){

        case "外資買賣超":
        case "投信買賣超":
        case "自營買賣超":
        case "三大法人買賣超":
            element.disabled = true;
            $(".user-choices").append('<div class="firm-variable"><span id="firmAttr">'+ firmAttr.slice(0, -3) + '</span><span>連續' +'</span><select class="form-select form-select-sm" aria-label=".form-select-sm example" style="width: 20%; display:inline-block;"><option value="buy">買超</option><option value="sell">賣超</option></select><select class="form-select form-select-sm" aria-label=".form-select-sm example" style="width: 15%; display:inline-block;"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select><span>　個月</span><button type="button" class="btn btn-secondary" style="display:inline-block;" onclick="removeCondition(this)"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-left" viewBox="0 0 16 16"><path d="M10 12.796V3.204L4.519 8 10 12.796zm-.659.753-5.48-4.796a1 1 0 0 1 0-1.506l5.48-4.796A1 1 0 0 1 11 3.204v9.592a1 1 0 0 1-1.659.753z"/></svg></button></div>');
            break;

        case "融資":
        case "融券":
            element.disabled = true;
            $(".user-choices").append('<div class="firm-variable"><span id="firmAttr">'+ firmAttr + '</span><span>連續' +'</span><select class="form-select form-select-sm" aria-label=".form-select-sm example" style="width: 20%; display:inline-block;"><option value="buy">增加</option><option value="sell">減少</option></select><select class="form-select form-select-sm" aria-label=".form-select-sm example" style="width: 20%; display:inline-block;"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select><span>　個月</span><button type="button" class="btn btn-secondary" style="display:inline-block;" onclick="removeCondition(this)"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-left" viewBox="0 0 16 16"><path d="M10 12.796V3.204L4.519 8 10 12.796zm-.659.753-5.48-4.796a1 1 0 0 1 0-1.506l5.48-4.796A1 1 0 0 1 11 3.204v9.592a1 1 0 0 1-1.659.753z"/></svg></button></div>');
            break;

        case "本益比":
            element.disabled = true;
            $(".user-choices").append('<div class="firm-variable"><span id="firmAttr">'+ firmAttr + '</span><select class="form-select form-select-sm" aria-label=".form-select-sm example" style="width: 20%; display:inline-block;"><option value="buy">大於</option><option value="sell">小於</option></select><select class="form-select form-select-sm" aria-label=".form-select-sm example" style="width: 20%; display:inline-block;"><option value="8">8</option><option value="12">12</option><option value="16">16</option></select><button type="button" class="btn btn-secondary" style="display:inline-block;" onclick="removeCondition(this)"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-left" viewBox="0 0 16 16"><path d="M10 12.796V3.204L4.519 8 10 12.796zm-.659.753-5.48-4.796a1 1 0 0 1 0-1.506l5.48-4.796A1 1 0 0 1 11 3.204v9.592a1 1 0 0 1-1.659.753z"/></svg></button></div>');
            break;

        case "股價淨值比":
            element.disabled = true;
            $(".user-choices").append('<div class="firm-variable"><span id="firmAttr">'+ firmAttr + '</span><select class="form-select form-select-sm" aria-label=".form-select-sm example" style="width: 20%; display:inline-block;"><option value="buy">大於</option><option value="sell">小於</option></select><select class="form-select form-select-sm" aria-label=".form-select-sm example" style="width: 20%; display:inline-block;"><option value="0.5">0.5</option><option value="1">1</option><option value="1.5">1.5</option></select><button type="button" class="btn btn-secondary" style="display:inline-block;" onclick="removeCondition(this)"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-left" viewBox="0 0 16 16"><path d="M10 12.796V3.204L4.519 8 10 12.796zm-.659.753-5.48-4.796a1 1 0 0 1 0-1.506l5.48-4.796A1 1 0 0 1 11 3.204v9.592a1 1 0 0 1-1.659.753z"/></svg></button></div>');
            break;

        case "現金殖利率":
            element.disabled = true;
            $(".user-choices").append('<div class="firm-variable"><span id="firmAttr">'+ firmAttr + '</span><select class="form-select form-select-sm" aria-label=".form-select-sm example" style="width: 20%; display:inline-block;"><option value="buy">大於</option><option value="sell">小於</option></select><select class="form-select form-select-sm" aria-label=".form-select-sm example" style="width: 20%; display:inline-block;"><option value="4">4</option><option value="6">6</option><option value="8">8</option></select><span>%</span><button type="button" class="btn btn-secondary" style="display:inline-block;" onclick="removeCondition(this)"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-left" viewBox="0 0 16 16"><path d="M10 12.796V3.204L4.519 8 10 12.796zm-.659.753-5.48-4.796a1 1 0 0 1 0-1.506l5.48-4.796A1 1 0 0 1 11 3.204v9.592a1 1 0 0 1-1.659.753z"/></svg></button></div>');
            break;

        default:
            haveMatched = false;

        }
        if (haveMatched) {
            const choicesList = document.querySelector(".user-choices");
            let removieButton = choicesList.querySelectorAll("button");

            for (let i = 0; i < removieButton.length; i++) {
                removieButton[i].addEventListener('click', function (e) {
                    e.preventDefault();
                    e.target.closest('div').remove();
                });
            }
        }
    }
    console.log(alreadyHave.length);
}

// remove condition
function removeCondition(element){

    var firmAttr = element.parentNode.querySelector("span").textContent;
    let conditionDivList = conditionsList.querySelectorAll("div");

    for (let i = 0; i < conditionDivList.length; i++) {

        firmVariableName = conditionDivList[i].querySelector("span").textContent
        console.log('可選的->', firmVariableName.slice(0, 5))
        console.log('已選的->', firmAttr)

        if (firmVariableName == firmAttr
            || firmVariableName.slice(0, 2) == firmAttr
            || firmVariableName.slice(0, 4) == firmAttr
            ) {
            conditionDivList[i].querySelector("button").disabled = false;
        };
    };
};

// filter data
$("#filterStcok").click(function(){

    const divList = document.querySelectorAll(".firm-variable");
    var dictOfCondition = {};

    $(".result").empty();

    for (let i=0; i < divList.length; i++){

        var firmAttr = divList[i].querySelector("#firmAttr");
        var selections = divList[i].querySelectorAll("select");
        dictOfCondition[firmAttr.textContent] = [];

        for (let j=0; j < selections.length; j++){

            var selectResult = [];
            var currentSelection = selections[j];
            var optionForCurrentSelection = currentSelection.options[currentSelection.selectedIndex].textContent;

            dictOfCondition[firmAttr.textContent].push(optionForCurrentSelection);

        };

    };

    $.ajax({
        url:'',
        type:'get',
        data:{
            conditions:JSON.stringify(dictOfCondition),
        },
        success:function(response){

            const totalResponse = Object.keys(response.conditionResult).length;

            // if there are qualified symbols, then return table.
            if (totalResponse > 0){
                var tableHead = Object.keys(response.conditionResult[0]);
                var tableValue = "";

                tableValue += '<table id="dtBasicExample"'
                tableValue += 'class="table table-striped table-bordered table-sm" cellspacing="0" width="100%">'

                // tabel header
                tableValue += '<thead>'
                for (let i=0; i<tableHead.length; i++){
                    tableValue += '<th class="th-sm">' + tableHead[i] + '</th>'
                };
                tableValue += '</thead>'

                // tabel rows
                for (let i=0; i<totalResponse; i++){

                        var currentRow = Object.values(response.conditionResult[i])
                        var linkToSymbolInfo = `../info/${currentRow[0]}`

                        tableValue += '<tr>'
                        tableValue += `<td><a id="symbol" href="${linkToSymbolInfo}" target="_blank">` + currentRow[0] + '</a></td>'
                        for (let j=1; j<currentRow.length; j++){
                            tableValue += '<td>' + currentRow[j] + '</td>'
                        }
                        tableValue += '</tr>'
                    }

                tableValue += '</table>'

                $(".result").append(tableValue);


                // function for interactive table, sorting, searching...
                $(document).ready(function () {
                    $('#dtBasicExample').DataTable({
                        language: {
                            url: 'https://cdn.datatables.net/plug-ins/1.10.24/i18n/Chinese-traditional.json'
                        }
                    });
                    $('.dataTables_length').addClass('bs-select');
                });
            }
            // return No qualified resulf information.
            else{
                $(".result").append('<h4 style="text-align:center; margin-top:5%">無符合條件結果..</h4>');
            }
        }
    });
});




