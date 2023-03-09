function Ordering()
%Celem tego przykladu jest zilustrowaie formatu macierzy oraz zilustrowanie jak tworzy sie reordering
%kluczowe linijki to: 
% tworzenie macierzy w formacie rzadkim linijka 63
% rysowanie macierzy w formacie rzadkim przed reorderingiem linia 65-66
% mierzenie czasu LU faktoryzacji przed reorderingiem linie 68-71
% przykladowe tworzenie reorderingu linia 75-88
% zaaplikowanie reorderingu na podstawie wektora replace(1:NZ) linia 90-98
% rysowanie macierzy w formacie rzadkim po reorderingu linia 100-101
% mierzenie czasu LU faktoryzacji po reorderingu linie 103-106

% PROSZE STWORZYÆ MACIERZ Z PRZEKATNA i SWOIM INICJALEM. 
% PROSZE STWORZYC PERMUTACJE KTORA ZNACZNIE ZREDUKUJE CZAS LU FAKTORYZACJI
% ZADANIE TO NALEZY WYKONAC W MALTAB LUB OCTAVE, TERMIN ODDANIA PIERWSZE CWICZENIA W STYCZNIU

  for r=2:10 %petla po rozmiarze macierzy
    N=3*(2^(r+1)-1); %rozmiar macierzy obliczamy na podstawie r
    k=1;
    for i=1:N
       matrix_i(k)=i;matrix_j(k)=i; matrix_v(k)=rand()+1; k=k+1;
       if i+1<N
         matrix_i(k)=i;matrix_j(k)=i+1; matrix_v(k)=rand()+1; k=k+1;
       endif       
    endfor
  
    istart=3*2^r+1;
    iend=N;
    rowinc=N/(iend-istart);
    c=istart;
    m=1;
    for i=1:N
      if c<N
        matrix_i(k)=i;matrix_j(k)=c; matrix_v(k)=rand()+1; k=k+1;
      endif
      if c+1<N
        matrix_i(k)=i;matrix_j(k)=c+1; matrix_v(k)=rand()+1; k=k+1;
      endif
      if c+2<N
        matrix_i(k)=i;matrix_j(k)=c+2; matrix_v(k)=rand()+1; k=k+1;
      endif
      m=m+1;
      if m>rowinc 
        c=c+1; m=1;
      endif      
    endfor
    k=k-1;
    matrix_ii(1:k)=matrix_i(1:k);
    matrix_ii(k+1:2*k)=matrix_j(1:k);
    
    matrix_jj(1:k)=matrix_j(1:k);
    matrix_jj(k+1:2*k)=matrix_i(1:k);

    %diagonal
    k=2*k;
    for i=1:N
      k=k+1;
      matrix_ii(k)=i;
      matrix_jj(k)=i;
    endfor

    matrix_vv(1:k)=rand()+1;
    %tworzenie sparse matrix w coordinate format
    S=sparse(matrix_ii,matrix_jj,matrix_vv);
    %rysowanie tej macierzy
    figure(1);
    if(r==5) spy(S,'bp',4); endif
    
    display('LU original');
    tic;
    lu(S);
    toc
    
    
%-> TUTAJ ROBIMY ODPOWIEDNI REORDERING
    %WE: r,p, N=3*2^(r+1)-1;
    ordering(1:N)=0;
    i=1; %pomocniczy index do postorder
    j=1; %index w tablicy ordering
    postorder(i,j,N);
    replace(1:N)=0;
    for i=1:N
      for j=1:N
        if ordering(j)==i
          replace(i)=j;
          break
        endif        
      endfor     
    endfor
    
    %aplikujemy reordering
    for i=1:k 
      ii=matrix_ii(i);
      jj=matrix_jj(i);
      matrix_ii(i)=replace(ii);
      matrix_jj(i)=replace(jj);
    endfor
    S=sparse(matrix_ii,matrix_jj,matrix_vv);
%<- TUTAJ ROBIMY ODPOWIEDNI REORDERING
    
    figure(2);
    if(r==5) spy(S,'bp',4); endif
        
    display('LU reorder');
    tic;
    lu(S);
    toc
    
  endfor
  %procedura tworzaca rekurencyjnie wektor permutacji
  %https://www.mdpi.com/2073-8994/12/12/2070
  function m = postorder(i,j,N)
    if 3*2*i<=N
      j=postorder(2*i,j,N);
    endif
    if 3*(2*i+1)<=N 
      j=postorder(2*i+1,j,N);  
    endif    
    jj=j;
    ii=N/3-i+1;
    ordering(3*(jj-1)+1)=3*(ii-1)+1;
    ordering(3*(jj-1)+2)=3*(ii-1)+2;
    ordering(3*(jj-1)+3)=3*(ii-1)+3;
    j=j+1;
    m=j;
  endfunction

endfunction
