import { useEffect, useMemo, useState } from 'react'
import './App.css'


const samples = [
  {
    id: 1,
    title: 'Moonlit Library',
    character: 'Lina',
    tags: ['portrait', 'library', 'warm light'],
    accent: 'amber',
    prompt:
      'masterpiece, best quality, 1girl, silver hair, moonlit library, warm candle light, detailed eyes',
    negativePrompt: 'low quality, blurry, bad anatomy, extra fingers',
  },
  {
    id: 2,
    title: 'Rainy Neon Street',
    character: 'Mika',
    tags: ['cyberpunk', 'rain', 'city'],
    accent: 'teal',
    prompt:
      'masterpiece, best quality, 1girl, short black hair, neon street, rain, reflective pavement',
    negativePrompt: 'worst quality, jpeg artifacts, bad hands, watermark',
  },
  {
    id: 3,
    title: 'Garden Tea Time',
    character: 'Noel',
    tags: ['garden', 'dress', 'soft color'],
    accent: 'rose',
    prompt:
      'masterpiece, best quality, 1girl, frilled dress, flower garden, afternoon tea, soft sunlight',
    negativePrompt: 'lowres, text, logo, missing fingers, deformed',
  },
]

function App() {
  const [query, setQuery] = useState('')
  const [copiedId, setCopiedId] = useState(null)

  const filteredSamples = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()
    if (!normalizedQuery) return samples

    return samples.filter((sample) => {
      const searchableText = [
        sample.title,
        sample.character,
        sample.prompt,
        sample.negativePrompt,
        ...sample.tags,
      ]
        .join(' ')
        .toLowerCase()

      return searchableText.includes(normalizedQuery)
    })
  }, [query])

  const copyPrompt = async (sample) => {
    const text = `${sample.prompt}\nNegative prompt: ${sample.negativePrompt}`

    try {
      await navigator.clipboard.writeText(text)
      setCopiedId(sample.id)
      window.setTimeout(() => setCopiedId(null), 1600)
    } catch {
      setCopiedId(null)
    }
  }

  useEffect(() => {
    async function fetchPrompts() {
      try {
        const response = await fetch('/prompts/')

        if (!response.ok) {
          throw new Error(`Failed to fetch prompts: ${response.status}`)
        }

        const prompts = await response.json()
        console.log(prompts)
      } catch (error) {
        console.error(error)
      }
    }

    fetchPrompts()
  }, [])

  async function handleSubmit(event) {
    event.preventDefault()

    try {
      const response = await fetch('/prompts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title,
          prompt_text: promptText,
        }),
      })

      if (!response.ok) {
        throw new Error(`Failed to create prompt: ${response.status}`)
      }

      const createdPrompt = await response.json()
      console.log('Created prompt:', createdPrompt)
    } catch (error) {
      console.error(error)
    }
  }

  const [title, setTitle] = useState('')
  const [promptText, setPromptText] = useState('')

  return (
    <main className="app-shell">
      <header className="top-bar">
        <div>
          <p className="eyebrow">NovelAI prompt manager</p>
          <h1>Prompt Gallery</h1>
        </div>
        <div className="summary-pill">{filteredSamples.length} images</div>
      </header>

      <form onSubmit={handleSubmit}>
        {/* ここに既存のタイトル・本文の入力欄を入れる */}

        <label>
          タイトル
          <input
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />
        </label>

        <label>
          プロンプト本文
          <textarea
            value={promptText}
            onChange={(event) => setPromptText(event.target.value)}
            rows={5}
          />
        </label>

        <p>入力した本文：{promptText}</p>

        <button type="submit">Submit</button>
      </form>

      <section className="toolbar" aria-label="Gallery filters">
        <label className="search-field">
          <span>Search</span>
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="prompt, tag, character"
          />
        </label>
      </section>

      <section className="gallery-grid" aria-label="Prompt gallery">
        {filteredSamples.map((sample) => (
          <article className="prompt-card" key={sample.id}>
            <div className={`art-preview ${sample.accent}`}>
              <div className="art-glow" />
              <div className="art-frame">
                <span>{sample.character}</span>
              </div>
            </div>

            <div className="card-body">
              <div className="card-heading">
                <div>
                  <h2>{sample.title}</h2>
                  <p>{sample.character}</p>
                </div>
                <button type="button" onClick={() => copyPrompt(sample)}>
                  {copiedId === sample.id ? 'Copied' : 'Copy'}
                </button>
              </div>

              <div className="tag-row">
                {sample.tags.map((tag) => (
                  <span key={tag}>{tag}</span>
                ))}
              </div>

              <p className="prompt-text">{sample.prompt}</p>
            </div>
          </article>
        ))}
      </section>
    </main>
  )
}

export default App
