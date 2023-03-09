function program5(n)
    for i=1:n %przekatna
       matrix_i(i) = i;
       matrix_j(i) = i;
       matrix_v(i) = rand()+1;
    end
    k = n+1;
    n16 = idivide(int32(n),16);
    n8 = idivide(int32(n),8);
    n4 = idivide(int32(n),4);
    n2 = idivide(int32(n),2);
    for i=n8:3*n8
       matrix_j(k) = n16;
       matrix_i(k) = i+n2;
       matrix_v(k) = rand()+1;
       k=k+1;
       matrix_j(k) = n4+n16;
       matrix_i(k) = i+n2;
       matrix_v(k) = rand()+1;
       k=k+1;
       matrix_j(k) = n2+n16;
       matrix_i(k) = i+n2;
       matrix_v(k) = rand()+1;
       k=k+1;
       
       matrix_i(k) = n16;
       matrix_j(k) = i+n2;
       matrix_v(k) = rand()+1;
       k=k+1;
       matrix_i(k) = n4+n16;
       matrix_j(k) = i+n2;
       matrix_v(k) = rand()+1;
       k=k+1;
       matrix_i(k) = n2+n16;
       matrix_j(k) = i+n2;
       matrix_v(k) = rand()+1;
       k=k+1;
       
       %
       matrix_i(k) = n8+n2+n4;
       matrix_j(k) = i+n4-n16;
       matrix_v(k) = rand()+1;
       k=k+1;
       matrix_i(k) = n2+n8;
       matrix_j(k) = i-n16;
       matrix_v(k) = rand()+1;
       k=k+1;
       
       matrix_j(k) = n8+n2+n4;
       matrix_i(k) = i+n4-n16;
       matrix_v(k) = rand()+1;
       k=k+1;
       matrix_j(k) = n2+n8;
       matrix_i(k) = i-n16;
       matrix_v(k) = rand()+1;
       k=k+1;
    end
    k = k-1;
    
    figure(1);
    s = sparse(matrix_i, matrix_j, matrix_v);
    spy(s, 'bp', 4);
    
    tic;
    lu(s);
    toc
    
    % reordering
    perm(1:n)=0;
    for i=1:n
        perm(i)=i;
    end
    
    % reordering
    visited(1:n)=false;
    for p=1:n
        cur=n+1;
        ix=-1;
        for x=1:n
            if ~visited(x)
                if cur>nnz(s(x,:))
                    ix=x;
                    cur=nnz(s(x,:));
                end
            end
        end
        % ix to pivot z minimalna liczba sasiadow
        visited(ix)=true;
        perm(p)=ix;
        [col, row]=find(s(ix,:));
        s(x,row(1))=0;
        for el=2:size(row)
            s(row(el),:)=s(row(el),:)+s(row(1),:);
            s(row(el),row(1))=0;
        end
    end
    
    %test = amd(s);
    
%-> TUTAJ ROBIMY ODPOWIEDNI REORDERING
    %WE: r,p, N=3*2^(r+1)-1;
    %ordering=test;
    ordering=perm;
    i=1; %pomocniczy index do postorder
    j=1; %index w tablicy ordering
    replace(1:n)=0;
    for i=1:n
      for j=1:n
        if ordering(j)==i
          replace(i)=j;
          break
        end       
      end      
    end 
    
    %aplikujemy reordering
    for i=1:k 
      ii=matrix_i(i);
      jj=matrix_j(i);
      matrix_i(i)=replace(ii);
      matrix_j(i)=replace(jj);
    end
    s=sparse(matrix_i,matrix_j,matrix_v);
%<- TUTAJ ROBIMY ODPOWIEDNI REORDERING
    

    figure(2);
    %s = sparse(matrix_i, matrix_j, matrix_v);
    spy(s, 'bp', 4);
    tic;
    lu(s);
    toc
end