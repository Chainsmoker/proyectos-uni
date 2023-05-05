const inputs = document.querySelectorAll(".form__group input")
const label = document.querySelectorAll(".form__group label")
const textarea = document.querySelector(".form__group textarea")
const form = document.querySelector("form")
const message = document.querySelector(".message__success")

for (let index = 0; index < inputs.length; index++) {
    inputs[index].addEventListener("focus", ()=>{
        label[index].classList.add("fijar")
    })

    inputs[index].addEventListener("blur", ()=>{
        if (inputs[index].value != "") return
        label[index].classList.remove("fijar")
    })

    textarea.addEventListener("focus", ()=>{
        label[label.length -1].classList.add("fijar")
    })

    textarea.addEventListener("blur", ()=>{
        if (inputs[index].value != "") return
        label[label.length -1].classList.remove("fijar")
    })
}
