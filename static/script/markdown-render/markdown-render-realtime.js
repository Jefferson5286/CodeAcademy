import {fromAsyncCodeToHtml} from 'https://esm.sh/@shikijs/markdown-it/async'
import MarkdownItAsync from 'https://esm.sh/markdown-it-async'
import {codeToHtml} from 'https://esm.sh/shiki'

let md

export async function InitRealtimeMarkdownRender(contentElement, previewElement) {
    md = MarkdownItAsync()
    md.use(fromAsyncCodeToHtml(codeToHtml, {
        themes: {
            dark: 'dracula',
            light: 'vitesse-light'
        },
        defaultColor: 'dark',
    }))
    contentElement.addEventListener('input', () => {
        RenderMarkdown(contentElement, previewElement)
    })
}

async function RenderMarkdown(contentElement, previewElement) {
    const markdown = contentElement.value
    previewElement.innerHTML = await md.renderAsync(markdown)
}