<script lang='ts'>
  import '../app.css';
  import { onMount } from 'svelte';
	import Navbar from './Navbar.svelte';
  import { themeChange } from 'theme-change';
	import SidePanel from './SidePanel.svelte';

  // NOTE: the element that is using one of the theme attributes must be in the DOM on mount
  onMount(() => {
    themeChange(false)
    // 👆 false parameter is required for svelte
  })

  let drawer = false;
</script>

<div class="drawer drawer-mobile">
  <input id="my-drawer" type="checkbox" class="drawer-toggle" bind:checked={drawer}/>

  <div class="drawer-content flex flex-col">

    <Navbar />  

    <!-- Page content here -->
    <slot />
  </div> 

  <SidePanel bind:drawer />
</div>

