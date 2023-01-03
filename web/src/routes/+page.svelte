<script>
  let numberOfCars = 0;
  let pageCount = 0;
</script>
<div class="card">
  <div class="card-body flex items-center text-center gap-8">
    <h2 class="card-title">Dashboard</h2>
    <div class="stats shadow w-full">
      <div class="stat">
        <div class="stat-title">Number of Cars</div>
        <div class="stat-value">{numberOfCars}</div>
      </div> 
      <div class="stat">
        <div class="stat-title">Pages Scraped</div>
        <div class="stat-value">{pageCount}</div>
      </div> 
    </div>
  </div>
</div>