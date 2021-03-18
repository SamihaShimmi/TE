


  @Override
  
  
    public
    int
  
  compareTo
  (
      
        
          Object
        
        o1
      
    )
  {
      
        
          
            int
          
          result
        ;
      // CASE 1 : Comparing to another Second object
      // -------------------------------------------
      
        if (
              o1
              instanceof
              Second
            )
          {
              
                
                  
                    Second
                  
                  s
                  = 
                      (
                      Second
                      )
                      o1
                    
                  
                ;
              
                if (
                      
                        this
                        .
                        firstMillisecond
                      
                      <
                      
                        s
                        .
                        firstMillisecond
                      
                    )
                  {
                      return 
                          -
                          1
                        ;
                    }
                
                else if (
                      
                        this
                        .
                        firstMillisecond
                      
                      >
                      
                        s
                        .
                        firstMillisecond
                      
                    )
                  {
                      return 
                          1
                        ;
                    }
                
                else {
                      return 
                          0
                        ;
                    }
                
              
            }
        
        // CASE 2 : Comparing to another TimePeriod object
        // -----------------------------------------------
        else if (
              o1
              instanceof
              RegularTimePeriod
            )
          {
              // more difficult case - evaluate later...
              
                
                  result
                  =
                  0
                ;
            }
        
        // CASE 3 : Comparing to a non-TimePeriod object
        // ---------------------------------------------
        else {
              // consider time periods to be ordered after general objects
              
                
                  result
                  =
                  1
                ;
            }
        
      
      return 
          result
        ;
    }


  