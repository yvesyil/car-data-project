<script lang='ts'>
  export let drawer;
</script>

<div class="drawer-side">
  <label for="my-drawer" class="drawer-overlay"></label> 
  <ul class="menu p-4 w-80 bg-base-100 text-base-content">
    <!-- Sidebar content here -->
    <li><a on:click={() => (drawer = false)} href="/">Dashboard</a></li>
    <li><a on:click={() => (drawer = false)} href="/cars">View Car Data</a></li>
    <li><a on:click={() => (drawer = false)} href="/cars/viz">Visualizations</a></li>
    <li><a on:click={() => (drawer = false)} href="/cars/add-car">Add a new Car</a></li>
    <li><a on:click={() => (drawer = false)} href="/file-upload">Upload a CSV File</a></li>
  </ul>
</div>