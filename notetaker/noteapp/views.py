from django.shortcuts import render, redirect


from .models import Document

def view(request, docid=None):
    documents = Document.objects.all()

    if request.method == "GET":
        title = request.GET.get("title")
        content = request.GET.get("content")

        if docid and docid > 0:
            document = Document.objects.get(pk=docid)
            document.title = title
            document.content = content

        else:
            return redirect('editor', docid=0)
    
    if docid and docid > 0:
        document = Document.objects.get(pk=docid)
    else:
        document = None
        docid = 0
    
    context = {
        "docid": docid,
        "documents": documents,
        "document": document
    }

    return render(request, "view.html", context)

def editor(request, docid):
    print("=== EDITOR VIEW CALLED ===")
    print(f"Method: {request.method}")
    print(f"POST data: {request.POST}")
    print(f"docid from URL: {docid}")
    
    documents = Document.objects.all()

    if request.method == "POST":
        docid = int(request.POST.get("docid", 0))
        title = request.POST.get("title")
        content = request.POST.get("content")

        if docid > 0:
             document = Document.objects.get(pk=docid)
             document.title = title
             document.content = content
             document.save()

             return redirect('view_note', docid=docid)
        else:
            document = Document.objects.create(title=title, content = content)

            return redirect('view_note', docid=document.id)
    
    if docid > 0:
        document = Document.objects.get(pk=docid)
    else:
        document = None
    context = {
        "docid": docid,
        "documents": documents,
        "document": document
    }

    return render(request, "editor.html", context)

def delete_document(request, docid):
    document = Document.objects.get(pk=docid)
    document.delete()

    return redirect('view')

