/* pdfUpload.js
   Handles PDF upload UI, client-side extraction fallback using PDF.js, and calls to dishAPI.extractFromPdf
*/

document.addEventListener('DOMContentLoaded', () => {
  const uploadBtn = document.getElementById('pdf-upload-btn');
  const fileInput = document.getElementById('pdf-upload-input');

  if (uploadBtn && fileInput) {
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handlePdfFile);
  }
});

async function handlePdfFile(e) {
  const file = e.target.files && e.target.files[0];
  if (!file) return;
  showLoading();

  try {
    // Prefer uploading to backend if endpoint exists
    try {
      const result = await dishAPI.extractFromPdf(file);
      if (result && result.recipe) {
        displayRecipeResults(result);
        showSuccess('Recipe extracted from PDF (server).');
        hideLoading();
        return;
      }
    } catch (serverErr) {
      console.warn('Server PDF extraction failed, falling back to client extraction', serverErr);
      // continue to client-side extraction
    }

    // Client-side extraction using PDF.js
    if (window.pdfjsLib) {
      const arrayBuffer = await file.arrayBuffer();
      const pdf = await window.pdfjsLib.getDocument({ data: arrayBuffer }).promise;
      let fullText = '';
      for (let i=1; i<=Math.min(pdf.numPages, 10); i++) {
        const page = await pdf.getPage(i);
        const txtContent = await page.getTextContent();
        const pageText = txtContent.items.map(it => it.str).join(' ');
        fullText += '\n' + pageText;
      }

      // Try backend text endpoint if available
      try {
        const textResult = await dishAPI.extractFromText(fullText);
        if (textResult && textResult.recipe) {
          displayRecipeResults(textResult);
          showSuccess('Recipe extracted from PDF (text upload).');
          hideLoading();
          return;
        }
      } catch (err) {
        console.warn('Text endpoint failed, attempting local parse.');
      }

      // Local naive parser fallback: find title, ingredient lines (simple heuristics)
      const recipe = parseRecipeFromText(fullText);
      if (recipe) {
        // Wrap into expected structure: { recipe: { ... }, dish: { name: recipe.title }}
        displayRecipeResults({ recipe, dish: { name: recipe.title || 'Extracted Recipe' } });
        showSuccess('Recipe extracted from PDF (client).');
      } else {
        showError('Could not extract structured recipe from PDF. Try a cleaner PDF or use recipe URL.');
      }
    } else {
      showError('PDF extraction not available (pdf.js missing).');
    }
  } catch (err) {
    console.error('PDF upload error:', err);
    showError(err.message || 'Error processing PDF');
  } finally {
    hideLoading();
  }
}

// naive parser for demonstration: finds lines starting with numbers or dashes as ingredients
function parseRecipeFromText(text) {
  if (!text || text.trim().length < 20) return null;
  const lines = text.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
  // title heuristics: first longish line
  const title = lines.find(l => l.length > 6 && l.length < 80) || 'Untitled Recipe';
  // find ingredient section lines by keywords
  const ingStartIndex = lines.findIndex(l => /ingredient/i.test(l) || /ingredients/i.test(l));
  let ingredients = [];
  if (ingStartIndex >= 0) {
    for (let i = ingStartIndex + 1; i < Math.min(lines.length, ingStartIndex + 80); i++) {
      const ln = lines[i];
      if (/instruction|direction|method|procedure/i.test(ln)) break;
      if (/^\d+(\.)?\s/.test(ln) || /^[-•*]/.test(ln) || /\b(tsp|tbsp|cup|g|gram|kg|ml|oz)\b/i.test(ln)) {
        ingredients.push({ name: ln.replace(/^[-•*\d\.\s]+/, ''), quantity: '', unit: '' });
      } else if (ingredients.length > 0 && ln.length < 60) {
        // short lines after ingredients probably belong to ingredients
        ingredients.push({ name: ln, quantity: '', unit: '' });
      }
    }
  }
  // instructions heuristics
  const instStartIndex = lines.findIndex(l => /instruction|direction|method|procedure|steps/i.test(l));
  const instructions = [];
  if (instStartIndex >= 0) {
    for (let i = instStartIndex + 1; i < Math.min(lines.length, instStartIndex + 200); i++) {
      const ln = lines[i];
      if (/^ingredient/i.test(ln)) break;
      if (ln.length > 10) instructions.push(ln);
    }
  }
  if (ingredients.length === 0 && instructions.length === 0) return null;
  return {
    id: 'pdf-client-' + Date.now(),
    servings: 1,
    source_url: null,
    summary: null,
    ingredients,
    instructions
  };
}
