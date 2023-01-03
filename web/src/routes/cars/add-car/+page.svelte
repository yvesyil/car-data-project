<script lang='ts'>
  let years: Array<number> = [];
  let currentYear = new Date().getFullYear();
  for (let y = currentYear; y >= currentYear - 100; y--) {
    years.push(y);
  }
  let engineSize = 1.5;
</script>

<div class="card">
  <div class="card-body items-center text-center gap-8">
    <h2 class="card-title">Add a new Car</h2>
    <form class="form-control flex flex-col items-center gap-8" method="POST" action="">
      <div class="grid grid-cols-2 gap-4">
        <label class="label" for="make">
          <span class="label-text">Make</span>
        </label>
        <input class="input input-bordered w-full max-w-xs" id="make" type="text" />
        <label class="label" for="model">
          <span class="label-text">Model</span>
        </label>
        <input class="input input-bordered w-full max-w-xs" id="model" type="text" />
        <label class="label" for="year">
          <span class="label-text">Year</span>
        </label>
        <select class="select select-bordered w-full max-w-xs" id="year">
          {#each years as year}
          <option value={year}>{year}</option>
          {/each}
        </select>
        <label class="label" for="description">
          <span class="label-text">Description</span>
        </label>
        <input class="input input-bordered w-full max-w-xs" id="description" type="text" />
        <label class="label" for="price">
          <span class="label-text">Price</span>
        </label>
        <label class="input-group">
          <select class="select select-bordered select-info">
            <option value="eur">€</option>
            <option value="usd">$</option>
          </select>
          <input class="input input-bordered" id="price" type="number" />
        </label>
        <label class="label" for="odometer">
          <span class="label-text">Odometer</span>
        </label>
        <label class="input-group">
          <input class="input input-bordered" id="odometer" type="number" />
          <select class="select select-bordered select-info">
            <option value="km">km</option>
            <option value="mile">mi</option>
          </select>
        </label>
        <label class="label" for="color">
          <span class="label-text">Color</span>
        </label>
        <input class="input input-bordered w-full max-w-xs" id="color" type="text" />
        <label class="label" for="transmission">
          <span class="label-text">Transmission</span>
        </label>
        <select class="select select-bordered w-full max-w-xs" id="transmission">
          <option value="automatic">Automatic</option>
          <option value="manual">Manual</option>
          <option value="hybrid">Hybrid</option>
        </select>
        <label class="label" for="fuel-type">
          <span class="label-text">Fuel Type</span>
        </label>
        <select class="select select-bordered w-full max-w-xs" id="fuel-type">
          <option value="petrol">Petrol</option>
          <option value="diesel">Diesel</option>
          <option value="hybrid">Hybrid</option>
          <option value="electric">Electric</option>
        </select>
        <label class="label" for="engine-size">
          <span class="label-text">Engine Size</span>
          <span class="label-text-alt">
            {#if engineSize == 5.1}
              5.0 &#x3C;
            {:else}
              {engineSize}
            {/if}
            L
          </span>
        </label>
        <div>
          <input class="range" id="engine-size" type="range" min="0" max="5.1" bind:value={engineSize} step="0.1" />
          <div class="w-full flex justify-between text-xs px-2">
            <span>0</span>
            <span>.5</span>
            <span>1.0</span>
            <span>1.5</span>
            <span>2.0</span>
            <span>2.5</span>
            <span>3.0</span>
            <span>3.5</span>
            <span>4.0</span>
            <span>4.5</span>
            <span>5.0 &#x3C;</span>
          </div>
        </div>
      </div>

      <input class="btn btn-primary" type="submit" value="Add" />
    </form>
  </div>
</div>