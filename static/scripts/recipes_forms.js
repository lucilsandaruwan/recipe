// recipe create

function add_ingradient(element) {
    /* the function to call from add ingradient link */
    // place holder for the new item number
    newIngNumber = "${newIngNumber}"
    // compose the html content to append to the page
    htmlString = `<div class="field-list">
    <div class="form-group-lable">Ingradiant ${newIngNumber}</div>
    <div class="form-group-wrapper">
      
        <div class="form-group ">
          <dt><label for="ingredients-${newIngNumber}-name">Name</label></dt>
          <dd><input id="ingredients-${newIngNumber}-name" name="ingredients-${newIngNumber}-name" required="" type="text" value="">
          
          </dd>
        </div>
      
        <div class="form-group ">
          <dt><label for="ingredients-${newIngNumber}-quantity">Quantity</label></dt>
          <dd><input id="ingredients-${newIngNumber}-quantity" name="ingredients-${newIngNumber}-quantity" required="" type="number" value="">
          
          </dd>
        </div>
      
        <div class="form-group ">
          <dt><label for="ingredients-${newIngNumber}-unit">Units</label></dt>
          <dd><input id="ingredients-${newIngNumber}-unit" name="ingredients-${newIngNumber}-unit" required="" type="text" value="">
          
          </dd>
        </div>
      
    </div>
    <div class="form-group-action"> <a href="#" onClick="delete_ingradient(this)"> Delete </a></div>
  </div>`;
  add_group_item(element, htmlString)
}

function add_method(element) {
    /* the function to call from add method step link */
    // place holder for the new item number
    newIngNumber = "${newIngNumber}"
    // compose the html content to append to the page
    htmlString = `<div class="field-list">
    <div class="form-group-lable"> Method, Step ${newIngNumber}</div>
    <div class="form-group-wrapper">
      
        <div class="form-group ">
          <dt><label for="methods-${newIngNumber}-title">Title</label></dt>
          <dd><input id="methods-${newIngNumber}-title" name="methods-${newIngNumber}-title" required="" type="text" value="">
          
          </dd>
        </div>
      
        <div class="form-group ">
          <dt><label for="methods-${newIngNumber}-discription">Description</label></dt>
          <dd><textarea id="methods-${newIngNumber}-discription" name="methods-${newIngNumber}-discription" required=""></textarea>
          
          </dd>
        </div>
      
    </div>
    <div class="form-group-action"> <a href="#" onclick="delete_ingradient(this)"> Delete </a></div>
  </div>`;
  add_group_item(element, htmlString)
}

function add_group_item(element, new_item) {
    /* this function will add new group item to field group block 
    */
    // stop default behavior of the item click
    event.preventDefault();
    // get the parent node of clicked link
    parentNode = element.parentNode;
    // get the grand parent node to find the field lists to get count
    gParentNode = parentNode.parentNode
    childNodes = gParentNode.querySelectorAll('.field-list');
    // calculate the new ingradient number using the list count
    newIngNumber = childNodes.length + 1
    // compose the html content to append to the page
    htmlString = new_item.replace("${newIngNumber}", newIngNumber);
    parentNode.insertAdjacentHTML('beforebegin', htmlString);
}

function delete_ingradient(element) {
    lableText = "Ingradiant "
    delete_group_item(element, lableText)
}

function delete_step(element) {
    lableText = "Method, step "
    delete_group_item(element, lableText)
}

function delete_group_item(element, lableText) {
    // stop default behavior of the item click
    event.preventDefault();
    parent = element.parentNode
    parentFieldList = parent.parentNode
    
    parentGroup = parentFieldList.parentNode
    listNodes = parentGroup.querySelectorAll('.field-list');

    // return if the form has only one ingradient
    // TODO: need to change the function to remove delete action link if there is only one ingradient remaining.
    if (listNodes.length == 1) {
        alert("You need to enter atleast one ingradient for the recipe");
        return
    }

    // remove the parent List node of the click element
    parentFieldList.remove()
    // this variable keep as the flag to identify elements after the removed element.
    // initially the value of this is false
    elefterRemovedElement = false;
    // loop the listNodes to change element values and attributes because of the removal of 
    // the element
    for(i = 0; i < listNodes.length; i ++) {
        // start the update the relevent attribute after changing the flag
        // this flag will be true for all the elements after the parent of click element
        if(elefterRemovedElement) {
            node = listNodes[i];
            console.log(node)
            ingradLableNode = node.querySelector(".form-group-lable");
            console.log(ingradLableNode)
            ingradLableNode.textContent = `${lableText} ${i}`;
            
        }
        // update the flag value to true if the parent node of click element is equal to the element in the list
        if(parentFieldList == listNodes[i]) {
            elefterRemovedElement = true;
        }
    }
    
}