from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Arquivo, Conteudo
from .forms import ArquivoForm
from .utils import get_pdf_text, get_docx_text, get_xlsx_text, get_pptx_text, get_text_chunks, create_and_store_embeddings, user_input, file_exists
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def Chatbot(request):
    return render(request, "interface/Chatbot.html")

@csrf_exempt
def upload_arquivo(request):
    if request.method == 'POST':
        substituir = request.POST.get('substituir', 'false') == 'true'
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = form.save(commit=False)
            arquivo.nome_do_arquivo = request.FILES['arquivo'].name
            
            nome_arquivo, extensao = os.path.splitext(arquivo.nome_do_arquivo)
            extensao = extensao[1:].lower()
            
            if extensao in ['pdf', 'docx', 'pptx', 'xlsx']:
                arquivo.tipo = extensao
                
                # Verifica se o arquivo já existe
                if file_exists(arquivo.nome_do_arquivo) and not substituir:
                    return JsonResponse({'duplicate': True, 'message': 'Arquivo já existe. Deseja substituir?'})
                
                # Se substituir for True, deletar o arquivo existente
                if substituir and file_exists(arquivo.nome_do_arquivo):
                    existing_file = Arquivo.objects.get(nome_do_arquivo=arquivo.nome_do_arquivo)
                    existing_file.delete()
                
                arquivo.save()
                
                try:
                    if extensao == 'pdf':
                        texto_extraido = get_pdf_text([arquivo.arquivo])
                    elif extensao in ['docx', 'doc']:
                        texto_extraido = get_docx_text([arquivo.arquivo])
                    elif extensao == 'pptx':
                        texto_extraido = get_pptx_text([arquivo.arquivo])
                    elif extensao == 'xlsx':
                        texto_extraido = get_xlsx_text([arquivo.arquivo])
                    
                    text_chunks = get_text_chunks(texto_extraido)
                    logger.debug(f"Text chunks created: {text_chunks}")
                    
                    create_and_store_embeddings(text_chunks, arquivo)
                    
                    messages.success(request, 'Arquivo enviado, texto extraído e embeddings geradas com sucesso')
                except Exception as e:
                    logger.error(f'Erro ao processar o arquivo: {str(e)}')
                    messages.error(request, f'Erro ao processar o arquivo: {str(e)}')
            else:
                messages.error(request, 'Tipo de arquivo inválido. Por favor, envie um arquivo com uma extensão válida.')
        else:
            messages.error(request, 'Ocorreu um erro ao enviar o arquivo. Por favor, tente novamente.')
    else:
        form = ArquivoForm()

    message = list(messages.get_messages(request))[0] if messages.get_messages(request) else None
    return JsonResponse({'message': str(message)})

@csrf_exempt
def consulta(request):
    if request.method == 'POST':
        consulta_texto = request.POST.get('consulta')
        conversation = request.session.get('conversation', [])
        if consulta_texto:
            resposta, conversation = user_input(consulta_texto, conversation)
            request.session['conversation'] = conversation
            return JsonResponse({'respostas': [resposta]})
        else:
            return JsonResponse({'error': 'Consulta não fornecida'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)
