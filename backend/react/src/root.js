var app = document.getElementById('app');
app.innerHTML = '<p>Hi There Mom,</p>';

if (module.hot) {
    module.hot.accept()
}