const rows = document.querySelectorAll("tbody tr");
let col1GlobalValue = "";


// Adding the "add button" in each department with expense_head and department data
rows.forEach(row => {
    const firstCol = row.querySelector("td:nth-child(1)");
    const innerHTMLValueCol1 = firstCol ? firstCol.innerHTML.trim() : "";
    const secondTd = row.querySelector("td:nth-child(2)");
    const innerHTMLValueCol2 = secondTd ? secondTd.innerHTML.trim() : "";

    if (secondTd && innerHTMLValueCol2) {
        secondTd.classList.add("button_text_td");
        secondTd.innerHTML += `<span class="button_group">                     
                                    <img this_is="accordion" class="disp_none" idToTargetRows="${innerHTMLValueCol1 ? `${innerHTMLValueCol1}_${innerHTMLValueCol2}` : `${col1GlobalValue}_${innerHTMLValueCol2}`}" src="arrowUpNDown.svg" alt="^">
                                    <img this_is="addButton" id="${innerHTMLValueCol1 ? `${innerHTMLValueCol1}_${innerHTMLValueCol2}` : `${col1GlobalValue}_${innerHTMLValueCol2}`}" src="addButton.svg" alt="+">
                                </span>`;
    }
    if (innerHTMLValueCol1) {
        col1GlobalValue = innerHTMLValueCol1;
    }
});

// Select all add buttons for event listener
const buttonImages = document.querySelectorAll('img[this_is="addButton"]');
const generalCaseColumn = `<td></td>
                    <td class="padding_0 disp_flex">
                        <input expense-name class="input_field_for_costing" type="text" name="" id="">
                        <img expense-remove src="minus-circle.svg" alt="-" > 
                    </td>`
const travelExpenseColumn = `<td></td>
                    <td class="padding_0 disp_flex">
                                <select expense-name class="input_field_for_costing"  name="" id="">
                                    <option value="">-----</option>
                                    <option value="IT">IT</option>
                                    <option value="Marketing">Marketing</option>
                                    <option value="Delivery">Delivery</option>
                                    <option value="Finance">Finance</option>
                                </select>
                        <img expense-remove src="minus-circle.svg" alt="-" > 
                    </td>`
const insertedRowsColumn =`
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td class="padding_0"><input class="input_field_for_costing" type="number" name="" id=""></td>
                    <td></td>`;

// Global array to store all `expense-name` inputs
let allExpenseNameInputs = [];

//to find the next sibling of deleted row

function getNextRowWithId(currentRow) {
    let nextRow = currentRow.nextElementSibling; // Start with the next sibling
    while (nextRow) {
        if (nextRow.hasAttribute('parent-table-rows')) { // Check if it has an 'id' attribute
            return nextRow; // Found the row with an 'id' attribute
        }
        nextRow = nextRow.nextElementSibling; // Move to the next sibling
    }
    return null; // No row with an 'id' attribute found
}


// Adding click event listener to each add button
buttonImages.forEach(button => {
    let lastInsertedRow = null; // Variable to keep track of the most recently added row
    let counter = 0;
    button.addEventListener('click', (event) => {
        const closestRow = event.target.closest('tr');
        const idOfClickedButton = event.target.id; // Get the ID of the clicked button

        // To display svg when row is added
        const closestSvg = closestRow.querySelector(`img[idToTargetRows="${idOfClickedButton}"]`);
        if (closestSvg) {
            closestSvg.classList.remove('disp_none');
        }

        // To insert row when the add button is clicked
        let nextRow = null;
        if (lastInsertedRow) {
            nextRow = lastInsertedRow.nextElementSibling;
        } else {
            nextRow = closestRow.nextElementSibling;
        }
        const ExistingRowsWithTargetedId = document.querySelectorAll(`tr[insertedRow="${idOfClickedButton}"]`);
        if(ExistingRowsWithTargetedId){
            ExistingRowsWithTargetedId.forEach(row=>{
                row.classList.remove('disp_none')
            })
        }

        const newRow = document.createElement('tr');
        newRow.setAttribute('insertedRow', idOfClickedButton);

        newRow.innerHTML = (idOfClickedButton !== "Travel Expenses_All Departments") ? generalCaseColumn + insertedRowsColumn + `<td>${counter}</td>` : travelExpenseColumn + insertedRowsColumn + `<td>${counter}</td>`;

        // Insert the new row at the appropriate position
        if (nextRow) {
            closestRow.parentNode.insertBefore(newRow, nextRow);
        } else {
            console.log("I rannnnnnnn")
            lastInsertedRow = null
            if (lastInsertedRow) {
                console.log("i have some value: ", lastInsertedRow)
                nextRow = lastInsertedRow.nextElementSibling;
                console.log(nextRow)
            } else {
                console.log("i have no value: ", lastInsertedRow, "next", closestRow.nextElementSibling )
                nextRow = getNextRowWithId(closestRow);
            }
            closestRow.parentNode.insertBefore(newRow, nextRow);
        }
        

         // Get the `expense-name` input from the newly inserted row and store it in the array
        const newExpenseNameInput = newRow.querySelector('input[expense-name] , select[expense-name]');
        if (newExpenseNameInput) {
            allExpenseNameInputs.push(newExpenseNameInput);
            addEventListenerToEveryExpenseInput()
            // console.log('All Expense Name Inputs:', allExpenseNameInputs); // Check the array's contents
        }




        // Update the lastInsertedRow to point to the newly inserted row
        lastInsertedRow = newRow;
        counter++;
    });
});

// Select all accordions and add event listener for opening/closing rows
const accordions = document.querySelectorAll('img[this_is="accordion"]');
accordions.forEach(accordion => {
    accordion.addEventListener('click', (event) => {
        // Use getAttribute to access the custom attribute correctly
        const targetedRowId = event.target.getAttribute('idToTargetRows');
        // Ensure that the attribute value is not null/undefined
        if (targetedRowId) {
            accordion.classList.toggle('add_rotation');
            const rowsWithTargetedId = document.querySelectorAll(`tr[insertedRow="${targetedRowId}"]`);
            rowsWithTargetedId.forEach(row => {
                row.classList.toggle('disp_none');
            });
            
        } else {
            accordion.classList.add('disp_none')
            if(accordion.classList.contains('add_rotation')){
                accordion.classList.remove('add_rotation')
            }
        }
    });
});

// add with class in all th and td from 3rd child

const row = document.querySelector('tr');
const cellsFromThirdToLast = row.querySelectorAll('td:nth-child(n+3), th:nth-child(n+3)');
cellsFromThirdToLast.forEach(cell => {
   cell.classList.add('width_5')
});

const allInputFields = document.querySelectorAll('.input_field_for_costing')
allInputFields.forEach(inp=>{
    const nearestTd = inp.closest('td')
    nearestTd.classList.add('padding_0')
})

// to manage minus sign 
const addEventListenerToEveryExpenseInput = ()=>{
    
    allExpenseNameInputs.forEach(allExpenseNameInput => {
        const nearestTd = allExpenseNameInput.closest('td');
        const nearestTr = allExpenseNameInput.closest('tr');
        const idToFindParentTr =  nearestTr.getAttribute('insertedRow');
        const accordionOfParentTr = document.querySelector(`img[idToTargetRows="${idToFindParentTr}"]`);
        const parentTrOfNearestTr = accordionOfParentTr.closest('tr')
        // console.log("parentTrOfNearestTr: ", parentTrOfNearestTr)
        const expenseRemove = nearestTd.querySelector('[expense-remove]');
        const nearestTrNextParentTr = getNextRowWithId(nearestTr)
        allExpenseNameInput.addEventListener('input', () => {
            if (allExpenseNameInput.value.trim() !== '') {
                if (!expenseRemove.classList.contains('disp_none')) {
                    console.log("add class disp_none")
                    expenseRemove.classList.add('disp_none');
                }
            } else {
                expenseRemove.classList.remove('disp_none');
            }
        });
        if(!expenseRemove.classList.contains('disp_none')){
            expenseRemove.addEventListener('click', ()=>{
                nearestTr.remove()
                allExpenseNameInputs = allExpenseNameInputs.filter(input => input !== allExpenseNameInput);
                console.log(allExpenseNameInputs);
                if(nearestTrNextParentTr === parentTrOfNearestTr.nextElementSibling){
                    accordionOfParentTr.classList.add('disp_none');
                    console.log("nearest accordion ********************", accordionOfParentTr)
                  
                }
            })
        }

    });
}

