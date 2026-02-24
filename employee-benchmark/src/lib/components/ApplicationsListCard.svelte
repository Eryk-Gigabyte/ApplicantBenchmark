<script lang="ts">
  import { goto } from '$app/navigation';
  import type { Applicant, Provider } from '$lib/types/index';

  // Svelte 5 Props Definition
  let { providers = [], columns = [] } = $props<{
    providers: {
      provider: Provider;
      applications: Applicant[];
      metadata?: { answerTime?: number; tokens?: number };
    }[];
    columns: string[];
  }>();

  const formatTime = (ms?: number) => (typeof ms === 'number' ? `${ms}ms` : '—');
  const formatTokens = (t?: number) => (typeof t === 'number' ? String(t) : '—');

  const initials = (name: string) =>
    name
      .split(' ')
      .map((p) => p[0]?.toUpperCase() ?? '')
      .slice(0, 2)
      .join('');
</script>

{#if providers.length === 0}
  <div class="w-full max-w-4xl mx-auto">
    <div class="rounded-lg border border-white/20 bg-white/03 p-6 text-center text-sm text-white/70">
      Keine Ergebnisse vorhanden
    </div>
  </div>
{:else}
  <div class="grid gap-6 md:grid-cols-2">
    {#each providers as block (block.provider.name)}
      <section class="relative rounded-2xl p-6 bg-white/05 backdrop-blur-md border border-white/20 flex flex-col">
        
        <div class="flex items-start gap-4 mb-7">
          {#if block.provider.icon}
            <img src={block.provider.icon} alt={block.provider.name} class="w-10 h-10 object-contain" />
          {:else}
            <div class="w-10 h-10 rounded-md bg-white/06 flex items-center justify-center text-sm font-semibold text-white/90">
              {initials(block.provider.name)}
            </div>
          {/if}

          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-semibold text-white truncate">{block.provider.name}</h3>
            <div class="flex gap-4 mt-1">
              <p class="text-xs text-white/50">
                Zeit: <span class="text-white/80">{formatTime(block.metadata?.answerTime)}</span>
              </p>
              <p class="text-xs text-white/50">
                Tokens: <span class="text-white/80">{formatTokens(block.metadata?.tokens)}</span>
              </p>
            </div>
          </div>
        </div>

        <div class="mt-auto">
          <div class="grid mb-2 px-3" style="grid-template-columns: repeat({columns.length}, minmax(0, 1fr)) 40px;">
            {#each columns as col}
              <div class="text-[10px] font-bold uppercase tracking-wider text-white/40">
                {col}
              </div>
            {/each}
            <div class="text-[10px] font-bold uppercase tracking-wider text-white/40 text-right">
              View
            </div>
          </div>

          {#if block.applications && block.applications.length > 0}
            <div class="divide-y divide-white/05 rounded-xl border border-white/10 bg-black/20 overflow-hidden">
              {#each block.applications as app (app.applicant_id)}
                <div 
                  class="grid items-center hover:bg-white/05 transition-colors group" 
                  style="grid-template-columns: repeat({columns.length}, minmax(0, 1fr)) 40px;"
                >
                  {#each columns as col}
                    <div class="text-sm text-white/80 px-3 py-3 truncate">
                      {#if col === 'name'}
                        {app.name}
                      {:else if col === 'surname'}
                        {app.surname}
                      {:else if col === 'mail'}
                        {app.mail}
                      {:else if col === 'applicant_id'}
                        <span class="text-xs font-mono text-white/40">{app.applicant_id.slice(0, 8)}...</span>
                      {:else}
                        {(app as any)[col] ?? '—'}
                      {/if}
                    </div>
                  {/each}
                  
                  <div class="px-2 py-3 text-right">
                    <button 
                      onclick={() => goto(`/application-detail/${app.applicant_id}`)}
                      class="p-1.5 rounded-md hover:bg-white/10 text-white/40 hover:text-white transition-all"
                      title="Details öffnen"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>
                      </svg>
                    </button>
                  </div>
                </div>
              {/each}
            </div>
          {:else}
            <div class="px-3 py-8 text-center text-sm text-white/30 italic">
              Keine Daten extrahiert.
            </div>
          {/if}
        </div>
      </section>
    {/each}
  </div>
{/if}

<style>
  /* Verhindert Layout-Shift bei Hover */
  .truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>