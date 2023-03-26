
#this is the class for infinite ordinal below epsilon_0
class InfOrdinal():
    
    def __init__(self, exp_ord=1, coe =1, add_ord =0):

        """every ordinal alpha that is smaller than epsilon_0 can be expressed in the following way: 
        alpha=w^beta * n + gamma, where beta, gamma are ordinals smaller than epsilon_0 and n is a natural number
        """ 
        
        if not isinstance(exp_ord,(InfOrdinal,int)):
            raise TypeError("Wrong data type for exponent, should be int or an InfOrdinal but is: "+str(type(exp_ord)) )

        if not isinstance(coe,(int)):
            raise TypeError("Wrong data type for coefficient, should be an int but is: "+str(type(coe)) )

        if not isinstance(add_ord,(InfOrdinal,int)):
            raise TypeError("Wrong data type for added ordinal, should be int or an InfOrdinal but is: "+str(type(add_ord)) )

        if not (exp_ord > 0 ):
            raise ValueError("exponent has to be larger than 0" )
        
        if (coe <= 0 ):
            raise ValueError("multiplicator has to be larger than 0" )

        if (add_ord < 0 ):
            raise ValueError("added ordinal has to be larger or equal to 0" + str(add_ord))
        
        self.exp_ord=exp_ord

        self.coe=coe

        self.add_ord=add_ord
    
    #returns a copy of the ordinal
    def copy(self):
        return InfOrdinal(self.exp_ord,self.coe,self.add_ord)
    
    #This will be useful when comparing the ordinals
    def to_list(self):

        return [self.exp_ord,self.coe, self.add_ord]
    
    #an ordinal < e_0 is exactly a limit ordinal when it has no finite part
    def limit_ord(self):

        return self.finite_part()==0
    
    def __eq__(self, other_ordinal):
        
        if not isinstance(other_ordinal,InfOrdinal):
            return False
        
        return self.to_list()==other_ordinal.to_list()

    

    #returns the finite part of an ordinal
    def finite_part(self):
        
        w=InfOrdinal()

        working_ordinal=self.add_ord

        #loops through the ordinal until the finite part is reached
        while isinstance(working_ordinal, InfOrdinal):
            
            working_ordinal=working_ordinal.add_ord
        
        return working_ordinal
    
    #returns the predecessor of an ordinal (for limit ordinals it returns the ordinal )
    def pred(self):
        finite_pred = max(0, self.finite_part()-1)
        return self.limit_part() + finite_pred
    
    #return all the parts of the ordinal that aren't finite, so the parts that have a w**(a) on the right
    def limit_part(self):
        return_ordinal=self.copy()
        working_ordinal = return_ordinal
        

        while not isinstance(working_ordinal.add_ord, int):
            working_ordinal = working_ordinal.add_ord

        working_ordinal.add_ord=0
        

        return return_ordinal

    def __lt__(self,other):
        
        if not isinstance(other,(InfOrdinal,int)):
            raise TypeError("Can not compare ordinal to"+str(type(other)))

        if isinstance(other,int):
            return False
        
        return self.to_list() < other.to_list()

    def __gt__(self, other):

        if not isinstance(other,(InfOrdinal,int)):
            raise TypeError("Can not compare ordinal to"+str(type(other)))

        if isinstance(other,int):
            return True
        return self.to_list() > other.to_list()

    #return the len of the ordinal i.e the amount of coe that != 0
    def __len__(self):
        counter=0
        working_ordinal=self

        while not isinstance(working_ordinal, int):
         working_ordinal=working_ordinal.add_ord
         counter+=1
        
        counter+= min(working_ordinal,1) #0 if add_part is 0 o.w 1
        return counter
    
    
    def __add__(self,other):
        
        if isinstance(other,int):
            
            if other <0:
                raise TypeError("Can not add ordinal to "+ str(type(other)))
            
            return InfOrdinal(self.exp_ord, self.coe, self.add_ord+other)
        
        '''w**(a_n)*b_n+..+ w**(a_1)*b_1 + b_0 + w**(c)*d
        = w**(c_n)*d_n+..+ w**(c_i)*d_1 + d_0  if c > a_n
        
        w**(a_n)*b_n+..+ w**(a_1)*b_1 + b_0 + w**(c)*d
        =  w**(a_n)*b_n+..+ w**(a_i+c)*(b_i+d) .....+ b_0 for a_i=c 
        '''
        if (self.add_ord==0):

            if (self.exp_ord > other.exp_ord):
                return InfOrdinal(self.exp_ord, self.coe, self.add_ord+other)

            if (self.exp_ord == other.exp_ord):
                return InfOrdinal(self.exp_ord, self.coe+other.coe, self.add_ord)

            if (self.exp_ord < other.exp_ord):
                return other
            
        #This just splits up the add_ordinal in it's w components
        else:
            return InfOrdinal(self.exp_ord, self.coe, 0) + (self.add_ord+other)

    
    
    def __radd__(self,other):

        if isinstance(other, int):

            if other >= 0 :
                return self

        raise  TypeError("Can not add ordinal to "+str(type(other)))
    

    def __mul__(self,other):
        
        if not isinstance(other, (InfOrdinal,int)):
            raise TypeError("Can not add multiply with "+str(type(other)))

        if isinstance(other,int):
            
            if other==0:
                return 0
            
            #(w**(a_n)*b_n+..+ w**(a_1)*b_1 + b_0)*m)=w**(a_n * m)*b_n+..+ w**(a_1)*b_1 + b_0
            else:
                return InfOrdinal(self.exp_ord,self.coe*other,self.add_ord)

        else:
            '''
            (w**(a)*b+c*(w**(d)*e+ f)
            =w**(a+d)*e+ w**(a)*b+c*f
            where f and c are finite or infinite ordinals
            '''
            return (
                InfOrdinal(self.exp_ord+other.exp_ord,  
                        other.coe,
                        InfOrdinal(self.exp_ord,self.coe,self.add_ord)*other.add_ord)
            )

    def __rmul__(self, other):

        if not isinstance(other, int):
            raise TypeError("Can not mulitply ordinal and"+str(type(other)))
        
        if other==0:
            return 0
        
        #m*(w**(a_n)*b_n +....+ w**(a_1)*b_1+b_0)=w**(a_n)*b_n +....+ w**(a_1)*b_1+ m*b_0
        else:
            return self.limit_part() + other*self.finite_part()

    def __pow__(self,other):
        
        if not isinstance(other, (int,InfOrdinal)):
            raise ValueError("ordinal can be raised to the power of "+str(type(other)))
        
        if other<0:
            raise ValueError("Exponent has to be larger than 0")
        
        if isinstance(other, int):
            
            if other==0:
                return 1
            
            result=self.copy()
            
            #ord**n=ord*ord....*ord (n times)
            for i in range(1,other):
                result=result*self.copy()
            
            return result
        
        

        #(w**(a_n)*b_n+..w**(a_1)*b_1+b_0)**(w**(c_n)*d_n+..w**(c_1)*d_1+d_0)
        #=w**(a_n * (w**(c_n)*d_n+..w**(c_1)*d_1)) * b_0*d_0
        else:
            
            return InfOrdinal(self.exp_ord*other.limit_part(),1,0) * (self**(other.finite_part()))

    def __rpow__(self, other):
        
        if not isinstance(other, (int,InfOrdinal)):
            raise ValueError("ordinal exponent not defined for "+str(type(other)))
        
        if other <0:
            raise ValueError("can not raise a negative number to the power of an ordinal")
        
        #k**(w*a+b) = k**(w*a) * k**(b)= (k**w)**a + k**(b)=w**a + k**(b)
        if self.exp_ord==1:
            return InfOrdinal(self.coe, other**(self.add_ord), 0)
        
        #k**(w**(a)*b + n) = w**(w**(a-1) * b) * (n ** k)
        if isinstance(self.add_ord,int):

            if isinstance(self.exp_ord, int):
                help_ord=InfOrdinal(max(self.exp_ord-1,0),self.coe,0)
            
            else:
                help_ord=InfOrdinal(self.exp_ord.pred(),self.coe,0)
            return InfOrdinal(help_ord, other**(self.add_ord),0)
        
        #k**(w**(a_n)*b_n + .. + w**(a_1)*b_1 + b_0) =
        #k**(w**(a_n)*b_n * k**(w**(a_(n-1))*b_(n-1) + .. + w**(a_1)*b_1 + b_0)
        else:
            return other**InfOrdinal(self.exp_ord, (self.coe),0) * other**(self.add_ord)
    

    

    '''gives the ordinal back as a string of the form: "w**(exp_ord)*coe + add_ord"
    ommitts the exponent and coe if they are 1 and the add_ord when it is 0
    '''
    def __str__(self):
    
        ordinal_string="w"
        if (self.exp_ord>1):
            ordinal_string+="**("+str(self.exp_ord)+")"

        if (self.coe>1):
            ordinal_string+="*"+str(self.coe)

        if (self.add_ord>0):
            ordinal_string+=" + "+str(self.add_ord)
            
        return ordinal_string


    __repr__=__str__