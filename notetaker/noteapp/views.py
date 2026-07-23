from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password


from .models import Document

def view(request, docid=None):
    documents_qs = Document.objects.all().order_by("-created_at")

    documents_list = [
        {
            "id": doc.id,
            "title": doc.title,
            "created_at": doc.created_at.isoformat() if doc.created_at else None
        }
        for doc in documents_qs
    ]
    authenticated = False
    wrong_password = False
    
    if docid and docid > 0:
        document = Document.objects.get(pk=docid)
        if request.session.get(f'note_{docid}_auth'):
            authenticated = True
            requires_password = False
        else:
            requires_password = bool(document.password_hash)
    else:
        document = None
        requires_password = False
        docid = 0

    if request.method == "POST":
        submitted_pw = request.POST.get("password")
        if document and document.password_hash and check_password(submitted_pw, document.password_hash):
            request.session[f"note_{docid}_auth"] = True

            return redirect("view_note", docid=docid)
    else:
        wrong_password = True

    
    
    context = {
        "docid": docid,
        "documents_list": documents_list,
        "document": document if (not requires_password or authenticated) else None,
        "requires_password": requires_password and not authenticated,
        "wrong_password": wrong_password
    }

    return render(request, "view.html", context)

def editor(request, docid):
    print("=== EDITOR VIEW CALLED ===")
    print(f"Method: {request.method}")
    print(f"POST data: {request.POST}")
    print(f"docid from URL: {docid}")
    
    documents_qs = Document.objects.all().order_by("-created_at")
    documents_list = list(Document.objects.all().values('id', 'title', 'created_at'))

    if request.method == "POST":
        submitted_docid = int(request.POST.get("docid", 0))
        title = request.POST.get("title")
        content = request.POST.get("content")
        enable_pw = request.POST.get("enable_password")
        plain_pw = request.POST.get("password") 

        if submitted_docid > 0:
            document = Document.objects.get(pk=submitted_docid) 
        else:
            document = Document()
        
        document.title = title
        document.content = content

        if enable_pw and plain_pw:
            document.password_hash = make_password(plain_pw)
        else:
            document.password_hash = None

        document.save()
        return redirect("view_note", docid=document.id)

    if docid > 0:
        document = Document.objects.get(pk=docid)
    else:
        document = None
        
    context = {
        "docid": docid,
        "documents_list": documents_list,
        "document": document
    }

    return render(request, "editor.html", context)

def delete_document(request, docid):
    document = Document.objects.get(pk=docid)
    document.delete()

    return redirect('view')

