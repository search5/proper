/**
 * Created by jiho on 2016. 12. 15..
 */
function greeter(person: any) {
    return "Hello, " + person;
}

var user = "Jane User";

document.body.innerHTML = greeter(user); 