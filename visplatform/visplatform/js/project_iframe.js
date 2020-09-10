
mocha.setup({
ui: 'bdd',
fullTrace: false,
global:['jQuery'],
})
mocha.cleanReferencesAfterRun(false)

new window.VConsole()

    