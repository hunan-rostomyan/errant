// Scheduler is setTimeout with an ability to delay
// already scheduled tasks.


// 1. DEFINITION
// -------------
function Scheduler(freq) {  // freq in ms
  this.freq = freq;
  setInterval(this._main.bind(this), this.freq);
}

Scheduler.prototype._main = function() {
  if (this.t) {
    if (this.t === this.freq) {
      this.fn();
    }
    this.t -= this.freq;
  }
};

// Works just like setTimeout.
Scheduler.prototype.assign = function(fn, t) {
  if (t % this.freq !== 0) {
    throw new Error('assign(fn, t): t must be a multiple of freq');
  }
  this.fn = fn;
  this.t = this.max = t;
};

// Delay the task by t (if t < max) or max.
Scheduler.prototype.delay = function(t) {
  if (this.t) {
    this.t = Math.min(this.max, this.t + t);
  }
};