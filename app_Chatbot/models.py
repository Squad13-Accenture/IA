from django.db import models

class Arquivo(models.Model):
    id_arquivo = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=6, choices=[('pdf', 'PDF'), ('docx', 'DOCX'), ('pptx', 'PPTX'), ('xlsx', 'XLSX'), ('csv', 'CSV'), ('xls', 'XLS')])
    data_do_upload = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='uploads/')
    nome_do_arquivo = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.arquivo.name
    
    class Meta:
        db_table = 'arquivo'

class Conteudo(models.Model):
    id_conteudo = models.AutoField(primary_key=True)
    texto = models.TextField()
    id_arquivo_id = models.ForeignKey(Arquivo, on_delete=models.CASCADE, db_column='id_arquivo_id')
    embeddings = models.BinaryField(null=True)

    def __str__(self):
        return f"Conteudo do Arquivo: {self.id_arquivo_id.nome_do_arquivo}"
    
    class Meta:
        db_table = 'conteudo'
