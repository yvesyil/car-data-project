<script lang='ts'>
  let files: FileList;
  let result: Promise<void> | null = null;

  function readFile(file: File): Promise<string | null> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();  
      reader.onload = () => {
        resolve(<string> reader.result)
      };
      reader.onerror = reject;
      reader.readAsText(file);
    });
  }

  const handleUpload = async () => {
    const content = await readFile(files[0]);

    const res = await fetch('/file-upload', {
      method: 'POST',
      body: content
    });

    const response = await res.json();
    result = new Promise((resolve, reject) => {
      if (response.success) {
        resolve();
      } else {
        reject();
      }
    });
  }
</script>


<div class="card">
  <div class="card-body flex items-center text-center gap-8">
    <h2 class="card-title">Upload a CSV File</h2>
    <form class="form-control flex flex-col gap-8" method="POST" on:submit|preventDefault={handleUpload}>
      <input id="file" type="file" class="file-input w-full max-w-xs" accept=".csv" bind:files />

      {#if result}
        {#await result}
          <progress class="progress w-full"></progress>
        {:then}
          <div class="alert alert-success shadow-lg">
            <div>
              <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <span>File uploaded successfully!</span>
            </div>
          </div> 
        {:catch}
          <div class="alert alert-error shadow-lg">
            <div>
              <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <span>Error while uploding the file.<span>
            </div>
          </div>
        {/await}
      {/if}

      <input class="btn btn-primary" type="submit" value="Upload" />
    </form>
  </div>
</div>