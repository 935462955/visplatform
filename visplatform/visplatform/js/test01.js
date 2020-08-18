
var assert = chai.assert
describe('Array', function() {
  describe('#indexOf()', function() {
    console.log(this)
    this.slow(1000);
    it('should return -1 when the value is not present', function() {
      assert.equal(-1, [1,2,3].indexOf(5));
      assert.equal(-1, [1,2,3].indexOf(0));
    });
    it('title should be Modal title', function(){
      console.log(document.querySelector('#exampleModalLabel').innerHTML)
      assert.equal(document.querySelector('#exampleModalLabel').innerHTML,"Modal title")
    })
  });
});